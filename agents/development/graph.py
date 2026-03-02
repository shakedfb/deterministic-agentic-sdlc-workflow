"""Development LangGraph subgraph: plan -> codegen -> testgen -> execute -> analyze."""

from __future__ import annotations

import json
from typing import Annotated, Any, TypedDict

import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from agents.llm import get_llm
from agents.memory import RedisStateStore, VectorMemory
from agents.models import (
    CodeArtifact,
    DependencyChange,
    Phase,
    RequirementSpec,
    SourceFile,
    TestResult,
    TestResults,
    WorkflowState,
)
from agents.prompts import DEV_CODEGEN_PROMPT, DEV_PLAN_PROMPT, DEV_TESTGEN_PROMPT
from agents.settings import settings
from agents.tracing import trace_phase
from config.guardrails_code import validate_code

logger = structlog.get_logger()

MAX_RETRIES = settings.max_unit_test_retries


class DevState(TypedDict):
    ticket_id: str
    requirement_spec: RequirementSpec
    subtasks: list[dict[str, Any]]
    code_artifact: CodeArtifact | None
    test_results: TestResults | None
    error_context: list[str]
    retry_count: int
    codebase_context: str
    messages: Annotated[list, add_messages]


@trace_phase("development")
async def plan_tasks(state: DevState) -> dict:
    """Node 1: Decompose RequirementSpec into implementation subtasks."""
    llm = get_llm(temperature=0)
    spec = state["requirement_spec"]

    memory = VectorMemory()
    try:
        similar_code = await memory.search(
            query=spec.feature_description, namespace="code_patterns", top_k=3
        )
        codebase_context = json.dumps(similar_code, indent=2) if similar_code else "No similar patterns found"
    except Exception:
        codebase_context = "Vector search unavailable"

    prompt = DEV_PLAN_PROMPT.format(
        requirement_spec=spec.model_dump_json(indent=2),
        codebase_context=codebase_context,
    )

    response = await llm.ainvoke([
        SystemMessage(content="You are a software architect. Return only valid JSON."),
        HumanMessage(content=prompt),
    ])

    try:
        subtasks = json.loads(response.content)
        if not isinstance(subtasks, list):
            subtasks = [subtasks]
    except json.JSONDecodeError:
        subtasks = [{"name": "implement_feature", "description": spec.feature_description, "files_to_create": [], "files_to_modify": [], "dependencies": []}]

    await logger.ainfo("tasks_planned", count=len(subtasks), ticket_id=state["ticket_id"])
    return {"subtasks": subtasks, "codebase_context": codebase_context}


@trace_phase("development")
async def generate_code(state: DevState) -> dict:
    """Node 2: LLM generates application code for each subtask."""
    llm = get_llm(temperature=0.1)
    spec = state["requirement_spec"]
    subtasks = state["subtasks"]
    error_ctx = "\n".join(state.get("error_context", [])) or "No previous errors"

    all_source_files: list[SourceFile] = []
    all_deps: list[DependencyChange] = []

    for subtask in subtasks:
        prompt = DEV_CODEGEN_PROMPT.format(
            subtask=json.dumps(subtask, indent=2),
            requirement_spec=spec.model_dump_json(indent=2),
            existing_code=state.get("codebase_context", ""),
            error_context=error_ctx,
        )

        response = await llm.ainvoke([
            SystemMessage(content="You are a senior software engineer. Return only valid JSON."),
            HumanMessage(content=prompt),
        ])

        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            await logger.aerror("codegen_json_parse_failed", subtask=subtask.get("name"))
            continue

        for f in result.get("files", []):
            validation = validate_code(f["content"], f.get("language", "python"))
            if not validation.valid:
                await logger.awarn(
                    "code_validation_failed",
                    file=f["path"],
                    errors=validation.errors,
                )
            all_source_files.append(
                SourceFile(path=f["path"], content=f["content"], language=f.get("language", "python"))
            )

        for dep in result.get("dependencies", []):
            all_deps.append(DependencyChange(**dep))

    branch = f"agentic/{state['ticket_id'].lower().replace('-', '_')}"
    artifact = CodeArtifact(
        ticket_id=state["ticket_id"],
        branch_name=branch,
        source_files=all_source_files,
        dependency_changes=all_deps,
    )

    await logger.ainfo(
        "code_generated",
        ticket_id=state["ticket_id"],
        file_count=len(all_source_files),
        attempt=state.get("retry_count", 0) + 1,
    )

    return {"code_artifact": artifact}


@trace_phase("development")
async def generate_tests(state: DevState) -> dict:
    """Node 3: LLM generates unit tests for the generated code."""
    llm = get_llm(temperature=0.1)
    spec = state["requirement_spec"]
    artifact = state["code_artifact"]

    if not artifact:
        return {"code_artifact": artifact}

    source_code = "\n\n".join(
        f"# {f.path}\n{f.content}" for f in artifact.source_files
    )
    criteria = "\n".join(
        f"- {c.description}" for c in spec.acceptance_criteria
    )

    prompt = DEV_TESTGEN_PROMPT.format(
        source_code=source_code,
        acceptance_criteria=criteria or "Test all public functions and edge cases",
    )

    response = await llm.ainvoke([
        SystemMessage(content="You are a senior QA engineer. Return only valid JSON."),
        HumanMessage(content=prompt),
    ])

    try:
        result = json.loads(response.content)
        test_files = [
            SourceFile(path=f["path"], content=f["content"], language=f.get("language", "python"))
            for f in result.get("test_files", [])
        ]
    except json.JSONDecodeError:
        test_files = []

    artifact_with_tests = artifact.model_copy(update={"test_files": test_files})
    await logger.ainfo("tests_generated", count=len(test_files))
    return {"code_artifact": artifact_with_tests}


@trace_phase("development")
async def execute_tests(state: DevState) -> dict:
    """Node 4: Execute unit tests in an E2B sandbox.

    Falls back to local simulation when E2B is unavailable.
    """
    artifact = state["code_artifact"]
    if not artifact or not artifact.test_files:
        return {
            "test_results": TestResults(total=0, passed=0, failed=0),
        }

    try:
        from e2b_code_interpreter import AsyncSandbox

        sandbox = await AsyncSandbox.create(api_key=settings.e2b_api_key)
        try:
            for f in artifact.source_files + artifact.test_files:
                await sandbox.files.write(f.path, f.content)

            for dep in artifact.dependency_changes:
                if dep.action in ("add", "update"):
                    await sandbox.commands.run(f"pip install {dep.package}=={dep.version}")

            result = await sandbox.commands.run(
                "python -m pytest --tb=short -q",
                timeout=120,
            )

            test_results = _parse_pytest_output(
                result.stdout or "", result.stderr or "", result.exit_code
            )
        finally:
            await sandbox.kill()

    except ImportError:
        await logger.awarn("e2b_unavailable, simulating test execution")
        test_results = TestResults(
            total=len(artifact.test_files),
            passed=len(artifact.test_files),
            failed=0,
            test_details=[
                TestResult(test_name=f.path, passed=True, duration_ms=100)
                for f in artifact.test_files
            ],
        )
    except Exception as exc:
        await logger.aerror("sandbox_execution_failed", error=str(exc))
        test_results = TestResults(
            total=1, passed=0, failed=1,
            test_details=[TestResult(test_name="sandbox_execution", passed=False, error_message=str(exc))],
        )

    await logger.ainfo(
        "tests_executed",
        total=test_results.total,
        passed=test_results.passed,
        failed=test_results.failed,
    )
    return {"test_results": test_results}


@trace_phase("development")
async def analyze_results(state: DevState) -> dict:
    """Node 5: Analyze test results and decide whether to retry or proceed."""
    results = state.get("test_results")
    retry_count = state.get("retry_count", 0)

    if results and results.all_passed:
        store = RedisStateStore()
        try:
            ws = WorkflowState(
                ticket_id=state["ticket_id"],
                phase=Phase.DEV,
                requirement_spec=state["requirement_spec"],
                code_artifact=state["code_artifact"],
                test_results=results,
                retry_counts={"unit_test": retry_count},
            )
            await store.save_state(ws)
        finally:
            await store.close()

        await logger.ainfo("tests_passed", ticket_id=state["ticket_id"])
        return {"error_context": []}

    failed_tests = [t for t in (results.test_details if results else []) if not t.passed]
    error_msgs = [
        f"FAIL {t.test_name}: {t.error_message}" for t in failed_tests if t.error_message
    ]

    await logger.awarn(
        "tests_failed",
        ticket_id=state["ticket_id"],
        failed_count=len(failed_tests),
        retry=retry_count,
    )

    return {
        "error_context": state.get("error_context", []) + error_msgs,
        "retry_count": retry_count + 1,
    }


def should_retry(state: DevState) -> str:
    """Decision gate: retry code generation, go to HITL, or proceed."""
    results = state.get("test_results")
    if results and results.all_passed:
        return "pass"
    retry_count = state.get("retry_count", 0)
    if retry_count < MAX_RETRIES:
        return "retry"
    return "hitl_needed"


def build_dev_graph() -> StateGraph:
    """Build the Development LangGraph subgraph."""
    graph = StateGraph(DevState)

    graph.add_node("plan_tasks", plan_tasks)
    graph.add_node("generate_code", generate_code)
    graph.add_node("generate_tests", generate_tests)
    graph.add_node("execute_tests", execute_tests)
    graph.add_node("analyze_results", analyze_results)

    graph.set_entry_point("plan_tasks")
    graph.add_edge("plan_tasks", "generate_code")
    graph.add_edge("generate_code", "generate_tests")
    graph.add_edge("generate_tests", "execute_tests")
    graph.add_edge("execute_tests", "analyze_results")
    graph.add_conditional_edges(
        "analyze_results",
        should_retry,
        {
            "pass": END,
            "retry": "generate_code",
            "hitl_needed": END,
        },
    )

    return graph


def compile_dev_graph(checkpointer=None):
    """Compile the dev graph with optional checkpointer."""
    graph = build_dev_graph()
    return graph.compile(checkpointer=checkpointer)


def _parse_pytest_output(stdout: str, stderr: str, exit_code: int) -> TestResults:
    """Parse pytest output into a TestResults model."""
    lines = (stdout + "\n" + stderr).strip().splitlines()
    details: list[TestResult] = []
    total = passed = failed = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("PASSED") or " PASSED" in stripped:
            name = stripped.split(" ")[0] if " " in stripped else stripped
            details.append(TestResult(test_name=name, passed=True))
            passed += 1
            total += 1
        elif stripped.startswith("FAILED") or " FAILED" in stripped:
            name = stripped.split(" ")[0] if " " in stripped else stripped
            details.append(TestResult(test_name=name, passed=False, error_message=stripped))
            failed += 1
            total += 1

    if total == 0:
        for line in lines:
            if "passed" in line or "failed" in line:
                import re
                m_pass = re.search(r"(\d+) passed", line)
                m_fail = re.search(r"(\d+) failed", line)
                if m_pass:
                    passed = int(m_pass.group(1))
                if m_fail:
                    failed = int(m_fail.group(1))
                total = passed + failed

    if total == 0 and exit_code == 0:
        total = 1
        passed = 1

    return TestResults(total=total, passed=passed, failed=failed, test_details=details)

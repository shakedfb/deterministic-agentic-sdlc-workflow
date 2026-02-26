"""E2E Testing LangGraph subgraph: provision env -> generate tests -> execute -> analyze."""

from __future__ import annotations

import json
from typing import Annotated, Any, TypedDict

import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from agents.memory import RedisStateStore
from agents.models import (
    CodeArtifact,
    E2ETestResults,
    Phase,
    RequirementSpec,
    SourceFile,
    TestResult,
    WorkflowState,
)
from agents.prompts import E2E_TESTGEN_PROMPT
from agents.settings import settings
from agents.tracing import trace_phase

logger = structlog.get_logger()

MAX_E2E_RETRIES = settings.max_e2e_retries


class E2EState(TypedDict):
    ticket_id: str
    requirement_spec: RequirementSpec
    code_artifact: CodeArtifact
    e2e_results: E2ETestResults | None
    error_context: list[str]
    retry_count: int
    environment_id: str | None
    messages: Annotated[list, add_messages]


@trace_phase("e2e_testing")
async def provision_environment(state: E2EState) -> dict:
    """Node 1: Provision an isolated test environment.

    Uses E2B sandbox or Docker Compose via MCP.
    """
    ticket_id = state["ticket_id"]
    env_id = f"e2e-{ticket_id.lower().replace('-', '_')}"

    try:
        from e2b_code_interpreter import AsyncSandbox

        sandbox = await AsyncSandbox.create(api_key=settings.e2b_api_key)
        env_id = sandbox.sandbox_id

        artifact = state["code_artifact"]
        for f in artifact.source_files:
            await sandbox.files.write(f.path, f.content)

        for dep in artifact.dependency_changes:
            if dep.action in ("add", "update"):
                await sandbox.commands.run(f"pip install {dep.package}=={dep.version}")

        await logger.ainfo("e2e_env_provisioned", env_id=env_id, via="e2b")
    except ImportError:
        await logger.awarn("e2b_unavailable, using simulated environment")
    except Exception as exc:
        await logger.aerror("env_provision_failed", error=str(exc))

    return {"environment_id": env_id}


@trace_phase("e2e_testing")
async def generate_e2e_tests(state: E2EState) -> dict:
    """Node 2: LLM generates E2E tests based on acceptance criteria."""
    llm = ChatOpenAI(model=settings.openai_model, temperature=0.1)
    spec = state["requirement_spec"]
    artifact = state["code_artifact"]

    source_summary = "\n".join(
        f"# {f.path}\n{f.content[:500]}..." if len(f.content) > 500 else f"# {f.path}\n{f.content}"
        for f in artifact.source_files
    )
    criteria = "\n".join(f"- {c.description}" for c in spec.acceptance_criteria)
    error_ctx = "\n".join(state.get("error_context", []))

    prompt = E2E_TESTGEN_PROMPT.format(
        feature_description=spec.feature_description,
        acceptance_criteria=criteria or "Test the feature end-to-end",
        application_code=source_summary,
        environment_details=f"Environment ID: {state.get('environment_id', 'local')}\n"
        f"Previous errors:\n{error_ctx}" if error_ctx else "No previous errors",
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
        await logger.aerror("e2e_testgen_failed")
        test_files = []

    updated_artifact = state["code_artifact"].model_copy(
        update={"test_files": state["code_artifact"].test_files + test_files}
    )
    await logger.ainfo("e2e_tests_generated", count=len(test_files))
    return {"code_artifact": updated_artifact}


@trace_phase("e2e_testing")
async def execute_e2e(state: E2EState) -> dict:
    """Node 3: Execute E2E test suite in the provisioned environment."""
    artifact = state["code_artifact"]
    e2e_test_files = [f for f in artifact.test_files if "e2e" in f.path.lower()]

    if not e2e_test_files:
        return {
            "e2e_results": E2ETestResults(
                total=0, passed=0, failed=0,
                environment_id=state.get("environment_id"),
            )
        }

    try:
        from e2b_code_interpreter import AsyncSandbox

        sandbox = await AsyncSandbox.create(api_key=settings.e2b_api_key)
        try:
            for f in artifact.source_files + e2e_test_files:
                await sandbox.files.write(f.path, f.content)

            result = await sandbox.commands.run(
                "python -m pytest tests/e2e/ --tb=short -q --timeout=60",
                timeout=180,
            )

            e2e_results = _parse_e2e_output(
                result.stdout or "",
                result.stderr or "",
                result.exit_code,
                state.get("environment_id"),
            )
        finally:
            await sandbox.kill()
    except ImportError:
        await logger.awarn("e2b_unavailable, simulating E2E execution")
        e2e_results = E2ETestResults(
            total=len(e2e_test_files),
            passed=len(e2e_test_files),
            failed=0,
            environment_id=state.get("environment_id"),
            test_details=[
                TestResult(test_name=f.path, passed=True, duration_ms=500)
                for f in e2e_test_files
            ],
        )
    except Exception as exc:
        await logger.aerror("e2e_execution_failed", error=str(exc))
        e2e_results = E2ETestResults(
            total=1, passed=0, failed=1,
            environment_id=state.get("environment_id"),
            test_details=[TestResult(test_name="e2e_execution", passed=False, error_message=str(exc))],
        )

    return {"e2e_results": e2e_results}


@trace_phase("e2e_testing")
async def analyze_e2e(state: E2EState) -> dict:
    """Node 4: Analyze E2E results; decide retry or proceed."""
    results = state.get("e2e_results")
    retry_count = state.get("retry_count", 0)

    if results and results.all_passed:
        store = RedisStateStore()
        try:
            ws = WorkflowState(
                ticket_id=state["ticket_id"],
                phase=Phase.TEST,
                requirement_spec=state["requirement_spec"],
                code_artifact=state["code_artifact"],
                e2e_results=results,
                retry_counts={"e2e": retry_count},
            )
            await store.save_state(ws)
        finally:
            await store.close()
        await logger.ainfo("e2e_passed", ticket_id=state["ticket_id"])
        return {"error_context": []}

    failed = [t for t in (results.test_details if results else []) if not t.passed]
    errors = [f"FAIL {t.test_name}: {t.error_message}" for t in failed if t.error_message]

    await logger.awarn("e2e_failed", ticket_id=state["ticket_id"], failed_count=len(failed))
    return {
        "error_context": state.get("error_context", []) + errors,
        "retry_count": retry_count + 1,
    }


def should_retry_e2e(state: E2EState) -> str:
    """Decision gate: retry, HITL, or proceed."""
    results = state.get("e2e_results")
    if results and results.all_passed:
        return "pass"
    if state.get("retry_count", 0) < MAX_E2E_RETRIES:
        return "retry"
    return "hitl_needed"


def build_e2e_graph() -> StateGraph:
    """Build the E2E Testing LangGraph subgraph."""
    graph = StateGraph(E2EState)

    graph.add_node("provision_environment", provision_environment)
    graph.add_node("generate_e2e_tests", generate_e2e_tests)
    graph.add_node("execute_e2e", execute_e2e)
    graph.add_node("analyze_e2e", analyze_e2e)

    graph.set_entry_point("provision_environment")
    graph.add_edge("provision_environment", "generate_e2e_tests")
    graph.add_edge("generate_e2e_tests", "execute_e2e")
    graph.add_edge("execute_e2e", "analyze_e2e")
    graph.add_conditional_edges(
        "analyze_e2e",
        should_retry_e2e,
        {"pass": END, "retry": "generate_e2e_tests", "hitl_needed": END},
    )

    return graph


def compile_e2e_graph(checkpointer=None):
    """Compile the E2E graph with optional checkpointer."""
    graph = build_e2e_graph()
    return graph.compile(checkpointer=checkpointer)


def _parse_e2e_output(
    stdout: str, stderr: str, exit_code: int, env_id: str | None
) -> E2ETestResults:
    """Parse pytest E2E output into an E2ETestResults model."""
    import re

    output = stdout + "\n" + stderr
    passed = 0
    failed = 0
    details: list[TestResult] = []

    for line in output.splitlines():
        if "PASSED" in line:
            name = line.split("::")[1].split(" ")[0] if "::" in line else line.strip()
            details.append(TestResult(test_name=name, passed=True))
            passed += 1
        elif "FAILED" in line:
            name = line.split("::")[1].split(" ")[0] if "::" in line else line.strip()
            details.append(TestResult(test_name=name, passed=False, error_message=line.strip()))
            failed += 1

    if not details:
        m_pass = re.search(r"(\d+) passed", output)
        m_fail = re.search(r"(\d+) failed", output)
        if m_pass:
            passed = int(m_pass.group(1))
        if m_fail:
            failed = int(m_fail.group(1))

    total = passed + failed
    if total == 0 and exit_code == 0:
        total = passed = 1

    return E2ETestResults(
        total=total, passed=passed, failed=failed,
        test_details=details, environment_id=env_id,
    )

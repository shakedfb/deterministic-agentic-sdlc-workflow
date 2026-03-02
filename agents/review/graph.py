"""Review LangGraph subgraph: security -> scale -> reliability analysis.

Sequential 3-pass review with no internal retry cycles.
Critical findings route back to Development; HIGH findings require HITL.
"""

from __future__ import annotations

import json
from typing import Annotated, Any, TypedDict

import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from agents.llm import get_llm
from agents.memory import RedisStateStore
from agents.models import (
    CodeArtifact,
    Phase,
    ReviewFinding,
    ReviewReport,
    Severity,
    WorkflowState,
)
from agents.prompts import REVIEW_RELIABILITY_PROMPT, REVIEW_SCALE_PROMPT, REVIEW_SECURITY_PROMPT
from agents.tracing import trace_phase

logger = structlog.get_logger()


class ReviewState(TypedDict):
    ticket_id: str
    code_artifact: CodeArtifact
    review_report: ReviewReport | None
    sast_output: str
    messages: Annotated[list, add_messages]


def _code_to_string(artifact: CodeArtifact) -> str:
    """Concatenate all source files into a single string for review."""
    return "\n\n".join(
        f"# File: {f.path}\n```{f.language}\n{f.content}\n```"
        for f in artifact.source_files
    )


def _parse_findings(raw: dict, category: str) -> list[ReviewFinding]:
    """Parse LLM-produced findings into ReviewFinding models."""
    findings: list[ReviewFinding] = []
    for f in raw.get("findings", []):
        try:
            severity = Severity(f.get("severity", "info").lower())
        except ValueError:
            severity = Severity.INFO
        findings.append(
            ReviewFinding(
                category=category,
                severity=severity,
                title=f.get("title", "Untitled finding"),
                description=f.get("description", ""),
                file_path=f.get("file_path"),
                line_number=f.get("line_number"),
                recommendation=f.get("recommendation", ""),
            )
        )
    return findings


@trace_phase("review")
async def security_review(state: ReviewState) -> dict:
    """Pass 1: Security analysis — OWASP Top 10, injections, auth gaps."""
    llm = get_llm(temperature=0)
    code = _code_to_string(state["code_artifact"])
    sast_output = state.get("sast_output", "No SAST output available")

    # Attempt to run Semgrep if available
    try:
        from mcp_servers.semgrep.server import run_semgrep_on_code

        code_files = [
            {"path": f.path, "content": f.content}
            for f in state["code_artifact"].source_files
        ]
        semgrep_results = await run_semgrep_on_code(code_files)
        sast_output = json.dumps(semgrep_results, indent=2)
    except Exception as exc:
        await logger.awarn("semgrep_unavailable", error=str(exc))

    prompt = REVIEW_SECURITY_PROMPT.format(code=code, sast_output=sast_output)
    response = await llm.ainvoke([
        SystemMessage(content="You are a security engineer. Return only valid JSON."),
        HumanMessage(content=prompt),
    ])

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {"findings": [], "security_score": 50}

    findings = _parse_findings(result, "security")
    security_score = result.get("security_score", 50)

    report = state.get("review_report") or ReviewReport()
    report = report.model_copy(update={
        "findings": report.findings + findings,
        "security_score": security_score,
    })

    await logger.ainfo("security_review_complete", findings_count=len(findings), score=security_score)
    return {"review_report": report, "sast_output": sast_output}


@trace_phase("review")
async def scale_review(state: ReviewState) -> dict:
    """Pass 2: Scale analysis — N+1 queries, memory leaks, missing indexes."""
    llm = get_llm(temperature=0)
    code = _code_to_string(state["code_artifact"])

    prompt = REVIEW_SCALE_PROMPT.format(code=code)
    response = await llm.ainvoke([
        SystemMessage(content="You are a performance engineer. Return only valid JSON."),
        HumanMessage(content=prompt),
    ])

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {"findings": [], "scale_score": 50}

    findings = _parse_findings(result, "scale")
    scale_score = result.get("scale_score", 50)

    report = state["review_report"] or ReviewReport()
    report = report.model_copy(update={
        "findings": report.findings + findings,
        "scale_score": scale_score,
    })

    await logger.ainfo("scale_review_complete", findings_count=len(findings), score=scale_score)
    return {"review_report": report}


@trace_phase("review")
async def reliability_review(state: ReviewState) -> dict:
    """Pass 3: Reliability analysis — error handling, circuit breakers, idempotency."""
    llm = get_llm(temperature=0)
    code = _code_to_string(state["code_artifact"])

    prompt = REVIEW_RELIABILITY_PROMPT.format(code=code)
    response = await llm.ainvoke([
        SystemMessage(content="You are a site reliability engineer. Return only valid JSON."),
        HumanMessage(content=prompt),
    ])

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {"findings": [], "reliability_score": 50}

    findings = _parse_findings(result, "reliability")
    reliability_score = result.get("reliability_score", 50)

    report = state["review_report"] or ReviewReport()
    all_findings = report.findings + findings
    report = report.model_copy(update={
        "findings": all_findings,
        "reliability_score": reliability_score,
        "approved": not any(
            f.severity in (Severity.CRITICAL, Severity.HIGH) for f in all_findings
        ),
    })

    store = RedisStateStore()
    try:
        ws = WorkflowState(
            ticket_id=state["ticket_id"],
            phase=Phase.REVIEW,
            code_artifact=state["code_artifact"],
            review_report=report,
        )
        await store.save_state(ws)
    finally:
        await store.close()

    await logger.ainfo(
        "reliability_review_complete",
        findings_count=len(findings),
        score=reliability_score,
        approved=report.approved,
    )
    return {"review_report": report}


def review_gate(state: ReviewState) -> str:
    """Decision gate: route based on review findings severity."""
    report = state.get("review_report")
    if report is None:
        return "hitl_needed"
    if report.has_critical:
        return "critical"
    if report.has_high:
        return "hitl_needed"
    return "pass"


def build_review_graph() -> StateGraph:
    """Build the Review LangGraph subgraph."""
    graph = StateGraph(ReviewState)

    graph.add_node("security_review", security_review)
    graph.add_node("scale_review", scale_review)
    graph.add_node("reliability_review", reliability_review)

    graph.set_entry_point("security_review")
    graph.add_edge("security_review", "scale_review")
    graph.add_edge("scale_review", "reliability_review")
    graph.add_conditional_edges(
        "reliability_review",
        review_gate,
        {"pass": END, "critical": END, "hitl_needed": END},
    )

    return graph


def compile_review_graph(checkpointer=None):
    """Compile the review graph with optional checkpointer."""
    graph = build_review_graph()
    return graph.compile(checkpointer=checkpointer)

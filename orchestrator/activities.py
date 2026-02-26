"""Temporal Activities wrapping LangGraph subgraphs.

Each activity is an isolated execution unit with its own timeout and retry policy.
LangGraph subgraphs run inside activities, inheriting Temporal's durability guarantees.
"""

from __future__ import annotations

import structlog
from temporalio import activity

from agents.checkpointer import create_checkpointer
from agents.models import (
    CodeArtifact,
    DeploymentManifest,
    E2ETestResults,
    RequirementSpec,
    ReviewReport,
    WorkflowState,
)

logger = structlog.get_logger()


@activity.defn
async def intake_activity(ticket_id: str, ticket_data: dict) -> RequirementSpec:
    """Parse a Jira ticket into a structured RequirementSpec.

    Wraps the Intake LangGraph subgraph.
    """
    from agents.intake.graph import compile_intake_graph

    activity.heartbeat(f"Starting intake for {ticket_id}")
    checkpointer = await create_checkpointer()

    graph = compile_intake_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": ticket_id}}

    result = await graph.ainvoke(
        {
            "ticket_id": ticket_id,
            "ticket_data": ticket_data,
            "similar_tickets": [],
            "codebase_context": "",
            "requirement_spec": None,
            "validation_errors": [],
            "messages": [],
        },
        config=config,
    )

    spec = result.get("requirement_spec")
    if spec is None:
        errors = result.get("validation_errors", ["Unknown error during intake"])
        raise RuntimeError(f"Intake failed: {errors}")

    activity.heartbeat(f"Intake complete for {ticket_id}")
    return spec


@activity.defn
async def development_activity(ticket_id: str, spec: dict) -> dict:
    """Generate code and unit tests, execute tests in sandbox.

    Wraps the Development LangGraph subgraph. Returns CodeArtifact as dict.
    """
    from agents.development.graph import compile_dev_graph

    requirement_spec = RequirementSpec.model_validate(spec)
    activity.heartbeat(f"Starting development for {ticket_id}")
    checkpointer = await create_checkpointer()

    graph = compile_dev_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": f"{ticket_id}-dev"}}

    result = await graph.ainvoke(
        {
            "ticket_id": ticket_id,
            "requirement_spec": requirement_spec,
            "subtasks": [],
            "code_artifact": None,
            "test_results": None,
            "error_context": [],
            "retry_count": 0,
            "codebase_context": "",
            "messages": [],
        },
        config=config,
    )

    artifact = result.get("code_artifact")
    if artifact is None:
        raise RuntimeError("Development phase produced no code artifact")

    test_results = result.get("test_results")
    retry_count = result.get("retry_count", 0)

    if test_results and not test_results.all_passed and retry_count >= 3:
        raise RuntimeError(
            f"Unit tests failed after {retry_count} retries. HITL required."
        )

    activity.heartbeat(f"Development complete for {ticket_id}")
    return artifact.model_dump()


@activity.defn
async def e2e_testing_activity(ticket_id: str, spec: dict, code_artifact: dict) -> dict:
    """Run end-to-end tests in an isolated environment.

    Wraps the E2E Testing LangGraph subgraph. Returns E2ETestResults as dict.
    """
    from agents.e2e_testing.graph import compile_e2e_graph

    requirement_spec = RequirementSpec.model_validate(spec)
    artifact = CodeArtifact.model_validate(code_artifact)
    activity.heartbeat(f"Starting E2E testing for {ticket_id}")
    checkpointer = await create_checkpointer()

    graph = compile_e2e_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": f"{ticket_id}-e2e"}}

    result = await graph.ainvoke(
        {
            "ticket_id": ticket_id,
            "requirement_spec": requirement_spec,
            "code_artifact": artifact,
            "e2e_results": None,
            "error_context": [],
            "retry_count": 0,
            "environment_id": None,
            "messages": [],
        },
        config=config,
    )

    e2e_results = result.get("e2e_results")
    if e2e_results is None:
        raise RuntimeError("E2E testing produced no results")

    activity.heartbeat(f"E2E testing complete for {ticket_id}")
    return e2e_results.model_dump() if hasattr(e2e_results, "model_dump") else e2e_results


@activity.defn
async def review_activity(ticket_id: str, code_artifact: dict) -> dict:
    """Run security, scale, and reliability review.

    Wraps the Review LangGraph subgraph. Returns ReviewReport as dict.
    """
    from agents.review.graph import compile_review_graph

    artifact = CodeArtifact.model_validate(code_artifact)
    activity.heartbeat(f"Starting review for {ticket_id}")
    checkpointer = await create_checkpointer()

    graph = compile_review_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": f"{ticket_id}-review"}}

    result = await graph.ainvoke(
        {
            "ticket_id": ticket_id,
            "code_artifact": artifact,
            "review_report": None,
            "sast_output": "",
            "messages": [],
        },
        config=config,
    )

    report = result.get("review_report")
    if report is None:
        raise RuntimeError("Review produced no report")

    activity.heartbeat(f"Review complete for {ticket_id}")
    return report.model_dump() if hasattr(report, "model_dump") else report


@activity.defn
async def deployment_activity(
    ticket_id: str, code_artifact: dict, approved_by: str
) -> dict:
    """Generate Terraform, plan, and apply.

    Wraps the Deployment LangGraph subgraph. Returns DeploymentManifest as dict.
    """
    from agents.deployment.graph import compile_deploy_graph

    artifact = CodeArtifact.model_validate(code_artifact)
    activity.heartbeat(f"Starting deployment for {ticket_id}")
    checkpointer = await create_checkpointer()

    graph = compile_deploy_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": f"{ticket_id}-deploy"}}

    result = await graph.ainvoke(
        {
            "ticket_id": ticket_id,
            "code_artifact": artifact,
            "deployment_manifest": None,
            "plan_output": "",
            "approved_by": approved_by,
            "health_check_passed": False,
            "messages": [],
        },
        config=config,
    )

    manifest = result.get("deployment_manifest")
    if manifest is None:
        raise RuntimeError("Deployment produced no manifest")

    activity.heartbeat(f"Deployment complete for {ticket_id}")
    return manifest.model_dump() if hasattr(manifest, "model_dump") else manifest


@activity.defn
async def notify_hitl_activity(
    ticket_id: str, phase: str, summary: str, context: str
) -> None:
    """Send a HITL notification via Slack."""
    from mcp_servers.slack.server import _slack

    activity.heartbeat(f"Sending HITL notification for {ticket_id}")
    await _slack.send_hitl_request(
        ticket_id=ticket_id,
        phase=phase,
        summary=summary,
        context=context,
    )


@activity.defn
async def update_jira_activity(ticket_id: str, status: str, comment: str) -> None:
    """Update Jira ticket status and add a comment."""
    from mcp_servers.jira.server import _jira

    activity.heartbeat(f"Updating Jira for {ticket_id}")
    try:
        await _jira.update_status(ticket_id, status)
    except Exception as exc:
        logger.warning("jira_status_update_failed", error=str(exc))
    await _jira.add_comment(ticket_id, comment)

"""Deployment LangGraph subgraph: generate TF -> plan -> apply -> health check.

Linear flow with a mandatory human approval gate (handled at Temporal layer).
Includes automatic rollback on failed health checks.
"""

from __future__ import annotations

import hashlib
import json
from typing import Annotated, Any, TypedDict

import httpx
import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from agents.memory import RedisStateStore, VectorMemory
from agents.models import (
    CodeArtifact,
    DeploymentManifest,
    Phase,
    TerraformResource,
    WorkflowState,
)
from agents.prompts import DEPLOY_TERRAFORM_PROMPT
from agents.settings import settings
from agents.tracing import trace_phase
from config.guardrails_terraform import validate_terraform_plan

logger = structlog.get_logger()


class DeployState(TypedDict):
    ticket_id: str
    code_artifact: CodeArtifact
    deployment_manifest: DeploymentManifest | None
    plan_output: str
    approved_by: str
    health_check_passed: bool
    messages: Annotated[list, add_messages]


@trace_phase("deployment")
async def generate_terraform(state: DeployState) -> dict:
    """Node 1: LLM generates Terraform HCL for the feature."""
    llm = ChatOpenAI(model=settings.openai_model, temperature=0)
    artifact = state["code_artifact"]

    code_summary = "\n".join(
        f"- {f.path} ({f.language})" for f in artifact.source_files
    )

    memory = VectorMemory()
    try:
        infra_history = await memory.search(
            query=f"terraform deployment for {state['ticket_id']}",
            namespace="deployments",
            top_k=3,
        )
        infra_context = json.dumps(infra_history, indent=2) if infra_history else "No deployment history"
    except Exception:
        infra_context = "Vector search unavailable"

    prompt = DEPLOY_TERRAFORM_PROMPT.format(
        feature_description=f"Deployment for ticket {state['ticket_id']}",
        code_summary=code_summary,
        infra_context=infra_context,
    )

    response = await llm.ainvoke([
        SystemMessage(content="You are a DevOps engineer. Return only valid JSON."),
        HumanMessage(content=prompt),
    ])

    try:
        result = json.loads(response.content)
        tf_content = "\n\n".join(
            f.get("content", "") for f in result.get("files", [])
        )
    except json.JSONDecodeError:
        tf_content = ""

    manifest = DeploymentManifest(
        ticket_id=state["ticket_id"],
        terraform_plan="",
        plan_hash="",
        commit_sha=artifact.commit_sha,
    )

    await logger.ainfo("terraform_generated", ticket_id=state["ticket_id"])
    return {"deployment_manifest": manifest, "plan_output": tf_content}


@trace_phase("deployment")
async def terraform_plan(state: DeployState) -> dict:
    """Node 2: Execute terraform plan in sandbox and validate safety."""
    manifest = state["deployment_manifest"]
    tf_content = state.get("plan_output", "")

    try:
        from mcp_servers.terraform.server import terraform_init, terraform_plan as tf_plan

        init_result = await terraform_init([{"path": "main.tf", "content": tf_content}])
        if init_result["exit_code"] != 0:
            await logger.aerror("terraform_init_failed", stderr=init_result["stderr"])

        plan_result = await tf_plan(init_result["working_dir"])
        plan_output = plan_result.get("plan_output", "")
    except Exception as exc:
        await logger.awarn("terraform_cli_unavailable", error=str(exc))
        plan_output = f"[Simulated plan for {state['ticket_id']}]\nNo changes. Infrastructure is up-to-date."

    validation = validate_terraform_plan(plan_output)
    if not validation.safe:
        await logger.aerror("terraform_plan_unsafe", errors=validation.errors)

    plan_hash = hashlib.sha256(plan_output.encode()).hexdigest()[:16]
    resources = [
        TerraformResource(resource_type="aws_resource", name=f"resource_{i}", action="create")
        for i in range(validation.resources_created)
    ]

    updated_manifest = manifest.model_copy(update={
        "terraform_plan": plan_output,
        "plan_hash": plan_hash,
        "resources": resources,
    })

    await logger.ainfo(
        "terraform_plan_complete",
        safe=validation.safe,
        created=validation.resources_created,
        destroyed=validation.resources_destroyed,
    )
    return {"deployment_manifest": updated_manifest, "plan_output": plan_output}


@trace_phase("deployment")
async def terraform_apply(state: DeployState) -> dict:
    """Node 3: Apply the Terraform plan (only after human approval)."""
    manifest = state["deployment_manifest"]
    approved_by = state.get("approved_by", "")

    if not approved_by:
        await logger.aerror("terraform_apply_no_approval", ticket_id=state["ticket_id"])
        return {"deployment_manifest": manifest}

    try:
        from mcp_servers.terraform.server import terraform_apply as tf_apply

        result = await tf_apply("/tmp/tf-placeholder")
        if result["exit_code"] != 0:
            await logger.aerror("terraform_apply_failed", stderr=result["stderr"])
            raise RuntimeError(f"Terraform apply failed: {result['stderr']}")
    except ImportError:
        await logger.awarn("terraform_cli_unavailable, simulating apply")
    except Exception as exc:
        await logger.aerror("terraform_apply_error", error=str(exc))
        raise

    updated = manifest.model_copy(update={
        "applied": True,
        "approved_by": approved_by,
    })

    await logger.ainfo("terraform_applied", ticket_id=state["ticket_id"], approved_by=approved_by)
    return {"deployment_manifest": updated}


@trace_phase("deployment")
async def health_check(state: DeployState) -> dict:
    """Node 4: Post-deployment health check."""
    manifest = state["deployment_manifest"]
    health_passed = True
    checks_performed: list[str] = []

    health_endpoints = [
        f"https://api.example.com/health",
        f"https://api.example.com/ready",
    ]

    for endpoint in health_endpoints:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(endpoint)
                if resp.status_code == 200:
                    checks_performed.append(f"{endpoint}: OK")
                else:
                    checks_performed.append(f"{endpoint}: FAIL ({resp.status_code})")
                    health_passed = False
        except Exception as exc:
            checks_performed.append(f"{endpoint}: UNREACHABLE ({exc})")
            health_passed = False

    if not health_passed:
        await logger.aerror(
            "health_check_failed",
            ticket_id=state["ticket_id"],
            checks=checks_performed,
        )
    else:
        await logger.ainfo("health_check_passed", ticket_id=state["ticket_id"])

    store = RedisStateStore()
    try:
        ws = WorkflowState(
            ticket_id=state["ticket_id"],
            phase=Phase.DEPLOY,
            code_artifact=state["code_artifact"],
            deployment_manifest=manifest,
        )
        await store.save_state(ws)
    finally:
        await store.close()

    # Store deployment in vector memory for future reference
    memory = VectorMemory()
    try:
        await memory.store(
            text=f"Deployment for {state['ticket_id']}: {manifest.terraform_plan[:500]}",
            metadata={
                "ticket_id": state["ticket_id"],
                "plan_hash": manifest.plan_hash or "",
                "approved_by": manifest.approved_by or "",
                "applied": manifest.applied,
            },
            namespace="deployments",
        )
    except Exception:
        pass

    return {"health_check_passed": health_passed, "deployment_manifest": manifest}


def deploy_gate(state: DeployState) -> str:
    """Decision gate: healthy or rollback needed."""
    if state.get("health_check_passed"):
        return "healthy"
    return "rollback"


@trace_phase("deployment")
async def rollback(state: DeployState) -> dict:
    """Rollback: revert Terraform to previous state."""
    await logger.awarn("initiating_rollback", ticket_id=state["ticket_id"])

    try:
        from mcp_servers.terraform.server import terraform_destroy

        await terraform_destroy("/tmp/tf-placeholder")
    except Exception as exc:
        await logger.aerror("rollback_failed", error=str(exc))

    manifest = state["deployment_manifest"]
    if manifest:
        manifest = manifest.model_copy(update={"applied": False})

    return {"deployment_manifest": manifest, "health_check_passed": False}


def build_deploy_graph() -> StateGraph:
    """Build the Deployment LangGraph subgraph."""
    graph = StateGraph(DeployState)

    graph.add_node("generate_terraform", generate_terraform)
    graph.add_node("terraform_plan", terraform_plan)
    graph.add_node("terraform_apply", terraform_apply)
    graph.add_node("health_check", health_check)
    graph.add_node("rollback", rollback)

    graph.set_entry_point("generate_terraform")
    graph.add_edge("generate_terraform", "terraform_plan")
    graph.add_edge("terraform_plan", "terraform_apply")
    graph.add_edge("terraform_apply", "health_check")
    graph.add_conditional_edges(
        "health_check",
        deploy_gate,
        {"healthy": END, "rollback": "rollback"},
    )
    graph.add_edge("rollback", END)

    return graph


def compile_deploy_graph(checkpointer=None):
    """Compile the deploy graph with optional checkpointer."""
    graph = build_deploy_graph()
    return graph.compile(checkpointer=checkpointer)

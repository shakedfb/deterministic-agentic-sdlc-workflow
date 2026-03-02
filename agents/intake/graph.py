"""Intake LangGraph subgraph: parse ticket -> enrich context -> generate spec."""

from __future__ import annotations

import json
from typing import Annotated, Any, TypedDict

import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from agents.llm import get_llm
from agents.memory import RedisStateStore, VectorMemory
from agents.models import AcceptanceCriterion, Phase, RequirementSpec, WorkflowState
from agents.prompts import INTAKE_PARSE_PROMPT
from agents.tracing import trace_phase
from config.guardrails_spec import validate_requirement_spec

logger = structlog.get_logger()


class IntakeState(TypedDict):
    ticket_id: str
    ticket_data: dict[str, Any]
    similar_tickets: list[dict[str, Any]]
    codebase_context: str
    requirement_spec: RequirementSpec | None
    validation_errors: list[str]
    messages: Annotated[list, add_messages]


@trace_phase("intake")
async def parse_ticket(state: IntakeState) -> dict:
    """Node 1: Parse the Jira ticket data into structured fields.

    In production this calls the Jira MCP server. Here we accept
    pre-fetched ticket_data in state for testability.
    """
    ticket_data = state["ticket_data"]
    await logger.ainfo("parse_ticket", ticket_id=state["ticket_id"])
    return {"ticket_data": ticket_data}


@trace_phase("intake")
async def enrich_context(state: IntakeState) -> dict:
    """Node 2: Query vector DB for similar past tickets and codebase context."""
    memory = VectorMemory()
    ticket_text = json.dumps(state["ticket_data"])

    try:
        similar = await memory.search(
            query=ticket_text,
            namespace="tickets",
            top_k=3,
        )
    except Exception as exc:
        await logger.awarn("vector_search_failed", error=str(exc))
        similar = []

    codebase_context = ""
    if state["ticket_data"].get("affected_components"):
        codebase_context = f"Affected components: {', '.join(state['ticket_data']['affected_components'])}"

    return {
        "similar_tickets": similar,
        "codebase_context": codebase_context,
    }


@trace_phase("intake")
async def generate_spec(state: IntakeState) -> dict:
    """Node 3: LLM generates a structured RequirementSpec from the ticket data."""
    llm = get_llm(temperature=0)

    prompt = INTAKE_PARSE_PROMPT.format(
        ticket_data=json.dumps(state["ticket_data"], indent=2),
        similar_tickets=json.dumps(state["similar_tickets"], indent=2) if state["similar_tickets"] else "None available",
        codebase_context=state["codebase_context"] or "No codebase context available",
    )

    response = await llm.ainvoke([
        SystemMessage(content="You are a structured data extraction agent. Return only valid JSON."),
        HumanMessage(content=prompt),
    ])

    try:
        spec_data = json.loads(response.content)
        spec = RequirementSpec.model_validate(spec_data)
    except (json.JSONDecodeError, Exception) as exc:
        await logger.aerror("spec_generation_failed", error=str(exc))
        return {
            "requirement_spec": None,
            "validation_errors": [f"Failed to parse LLM response: {exc}"],
        }

    validation = validate_requirement_spec(spec.model_dump())
    if not validation.valid:
        await logger.awarn("spec_validation_failed", errors=validation.errors)
        return {
            "requirement_spec": spec,
            "validation_errors": validation.errors,
        }

    await logger.ainfo("spec_generated", ticket_id=spec.ticket_id, complexity=spec.complexity_score)

    store = RedisStateStore()
    try:
        workflow_state = WorkflowState(
            ticket_id=spec.ticket_id,
            phase=Phase.INTAKE,
            requirement_spec=spec,
        )
        await store.save_state(workflow_state)
    finally:
        await store.close()

    return {
        "requirement_spec": spec,
        "validation_errors": [],
    }


def spec_gate(state: IntakeState) -> str:
    """Decision gate: route based on spec validation results."""
    if state.get("validation_errors"):
        return "hitl_needed"
    if state.get("requirement_spec") is None:
        return "hitl_needed"
    return "pass"


def build_intake_graph() -> StateGraph:
    """Build the Intake LangGraph subgraph."""
    graph = StateGraph(IntakeState)

    graph.add_node("parse_ticket", parse_ticket)
    graph.add_node("enrich_context", enrich_context)
    graph.add_node("generate_spec", generate_spec)

    graph.set_entry_point("parse_ticket")
    graph.add_edge("parse_ticket", "enrich_context")
    graph.add_edge("enrich_context", "generate_spec")
    graph.add_conditional_edges(
        "generate_spec",
        spec_gate,
        {"pass": END, "hitl_needed": END},
    )

    return graph


def compile_intake_graph(checkpointer=None):
    """Compile the intake graph with optional checkpointer."""
    graph = build_intake_graph()
    return graph.compile(checkpointer=checkpointer)

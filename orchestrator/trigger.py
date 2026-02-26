"""CLI trigger for the SDLC workflow — starts a workflow from a Jira ticket ID."""

from __future__ import annotations

import argparse
import asyncio
import json

import structlog
from temporalio.client import Client

from agents.settings import settings
from orchestrator.workflow import SDLCWorkflow, WorkflowInput

logger = structlog.get_logger()


async def trigger_workflow(ticket_id: str, ticket_data: dict | None = None) -> str:
    """Start an SDLC workflow for a given Jira ticket.

    Returns the Temporal workflow run ID.
    """
    client = await Client.connect(
        settings.temporal_host,
        namespace=settings.temporal_namespace,
    )

    if ticket_data is None:
        from mcp_servers.jira.server import _jira
        issue = await _jira.get_issue(ticket_id)
        fields = issue.get("fields", {})
        ticket_data = {
            "key": issue["key"],
            "summary": fields.get("summary", ""),
            "description": fields.get("description", ""),
            "priority": fields.get("priority", {}).get("name", "Medium"),
            "labels": fields.get("labels", []),
        }

    workflow_input = WorkflowInput(ticket_id=ticket_id, ticket_data=ticket_data)

    handle = await client.start_workflow(
        SDLCWorkflow.run,
        workflow_input,
        id=f"sdlc-{ticket_id}",
        task_queue=settings.temporal_task_queue,
    )

    logger.info("workflow_started", ticket_id=ticket_id, run_id=handle.id)
    return handle.id


def main() -> None:
    parser = argparse.ArgumentParser(description="Trigger an SDLC workflow")
    parser.add_argument("--ticket-id", required=True, help="Jira ticket ID (e.g. PROJ-123)")
    parser.add_argument("--ticket-data", help="JSON string of ticket data (skips Jira fetch)")
    args = parser.parse_args()

    ticket_data = json.loads(args.ticket_data) if args.ticket_data else None
    run_id = asyncio.run(trigger_workflow(args.ticket_id, ticket_data))
    print(f"Workflow started: {run_id}")


if __name__ == "__main__":
    main()

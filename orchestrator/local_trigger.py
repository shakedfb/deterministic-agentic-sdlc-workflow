"""Plain-text CLI trigger — bypass Jira entirely.

Usage:
    python -m orchestrator.local_trigger "Build a REST API for user profiles"
    python -m orchestrator.local_trigger --file spec.txt
    python -m orchestrator.local_trigger --interactive
"""

from __future__ import annotations

import argparse
import asyncio
import random
import string
import sys

import structlog
from temporalio.client import Client

from agents.settings import settings
from orchestrator.workflow import SDLCWorkflow, WorkflowInput

logger = structlog.get_logger()


def _generate_ticket_id() -> str:
    """Generate a synthetic LOCAL-XXXXXX ticket ID."""
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"LOCAL-{suffix}"


def _build_ticket_data(
    description: str,
    title: str | None = None,
    priority: str = "Medium",
) -> dict:
    """Construct a ticket_data dict matching intake graph expectations."""
    return {
        "key": _generate_ticket_id(),
        "summary": title or description[:120],
        "description": description,
        "priority": priority,
        "labels": ["local-trigger"],
    }


async def trigger_local(
    description: str,
    title: str | None = None,
    priority: str = "Medium",
) -> str:
    """Start an SDLC workflow from a plain-text description.

    Returns the Temporal workflow run ID.
    """
    ticket_data = _build_ticket_data(description, title, priority)
    ticket_id = ticket_data["key"]

    client = await Client.connect(
        settings.temporal_host,
        namespace=settings.temporal_namespace,
    )

    workflow_input = WorkflowInput(ticket_id=ticket_id, ticket_data=ticket_data)

    handle = await client.start_workflow(
        SDLCWorkflow.run,
        workflow_input,
        id=f"sdlc-{ticket_id}",
        task_queue=settings.temporal_task_queue,
    )

    logger.info(
        "workflow_started",
        ticket_id=ticket_id,
        run_id=handle.id,
        source="local_trigger",
    )
    return handle.id


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Trigger an SDLC workflow from a plain-text feature description",
    )
    parser.add_argument(
        "description",
        nargs="?",
        help="Feature description (inline text)",
    )
    parser.add_argument(
        "--file", "-f",
        help="Read feature description from a file",
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Enter feature description interactively",
    )
    parser.add_argument(
        "--title", "-t",
        help="Short title for the feature (defaults to first 120 chars of description)",
    )
    parser.add_argument(
        "--priority", "-p",
        default="Medium",
        choices=["Low", "Medium", "High", "Critical"],
        help="Priority level (default: Medium)",
    )
    args = parser.parse_args()

    # Resolve description from the three input modes
    if args.interactive:
        print("Enter feature description (press Ctrl+D or Ctrl+Z when done):")
        description = sys.stdin.read().strip()
    elif args.file:
        with open(args.file) as f:
            description = f.read().strip()
    elif args.description:
        description = args.description
    else:
        parser.error("Provide a description, --file, or --interactive")
        return  # unreachable, satisfies type checker

    if not description:
        parser.error("Description cannot be empty")

    print(f"Starting SDLC workflow...")
    print(f"  Title: {args.title or description[:80]}...")
    print(f"  Priority: {args.priority}")
    print(f"  Provider: {settings.llm_provider} / {settings.llm_model or '(default)'}")
    print()

    run_id = asyncio.run(trigger_local(description, args.title, args.priority))

    print(f"Workflow started successfully!")
    print(f"  Run ID: {run_id}")
    print(f"  Temporal UI: http://localhost:8080/namespaces/{settings.temporal_namespace}/workflows")


if __name__ == "__main__":
    main()

"""Temporal Worker — runs the SDLC workflow and all activities."""

from __future__ import annotations

import asyncio

import structlog
from temporalio.client import Client
from temporalio.worker import Worker

from agents.settings import settings
from orchestrator.activities import (
    deployment_activity,
    development_activity,
    e2e_testing_activity,
    intake_activity,
    notify_hitl_activity,
    review_activity,
    update_jira_activity,
)
from orchestrator.workflow import SDLCWorkflow

logger = structlog.get_logger()


async def run_worker() -> None:
    """Connect to Temporal and start the worker."""
    client = await Client.connect(
        settings.temporal_host,
        namespace=settings.temporal_namespace,
    )

    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=[SDLCWorkflow],
        activities=[
            intake_activity,
            development_activity,
            e2e_testing_activity,
            review_activity,
            deployment_activity,
            notify_hitl_activity,
            update_jira_activity,
        ],
    )

    logger.info(
        "worker_starting",
        task_queue=settings.temporal_task_queue,
        namespace=settings.temporal_namespace,
    )
    await worker.run()


def main() -> None:
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()

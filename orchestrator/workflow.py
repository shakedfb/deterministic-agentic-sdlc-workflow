"""Temporal Workflow definition for the full SDLC pipeline.

The workflow orchestrates five phases as sequential activities:
  Intake -> Development -> E2E Testing -> Review -> Deployment

Each activity wraps a LangGraph subgraph. Temporal handles durability,
retries, timeouts, and human-in-the-loop signal waits.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger()


@dataclass
class HITLSignal:
    """Signal payload from human-in-the-loop interaction."""
    action: str  # "approve", "reject", "fix"
    payload: dict[str, Any] | None = None
    actor: str = ""


@dataclass
class WorkflowInput:
    """Input to the SDLC workflow."""
    ticket_id: str
    ticket_data: dict[str, Any]


@workflow.defn
class SDLCWorkflow:
    """Deterministic agentic SDLC workflow.

    Orchestrates the full pipeline from Jira ticket to production deployment.
    Uses Temporal signals for human-in-the-loop approval gates.
    """

    def __init__(self) -> None:
        self._hitl_signal: HITLSignal | None = None
        self._current_phase: str = "intake"

    @workflow.signal
    async def hitl_response(self, signal: HITLSignal) -> None:
        """Receive a human-in-the-loop response signal."""
        self._hitl_signal = signal

    @workflow.query
    def current_phase(self) -> str:
        """Query the current pipeline phase."""
        return self._current_phase

    @workflow.run
    async def run(self, input: WorkflowInput) -> dict[str, Any]:
        ticket_id = input.ticket_id
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(minutes=5),
            maximum_attempts=3,
        )

        # ── Phase 1: Intake ──────────────────────────────────────
        self._current_phase = "intake"
        workflow.logger.info(f"Starting intake for {ticket_id}")

        spec = await workflow.execute_activity(
            "intake_activity",
            args=[ticket_id, input.ticket_data],
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=retry_policy,
        )

        await workflow.execute_activity(
            "update_jira_activity",
            args=[ticket_id, "In Progress", "Agentic workflow: requirement spec generated."],
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=retry_policy,
        )

        # ── Phase 2: Development ─────────────────────────────────
        self._current_phase = "development"
        workflow.logger.info(f"Starting development for {ticket_id}")

        try:
            code_artifact = await workflow.execute_activity(
                "development_activity",
                args=[ticket_id, spec if isinstance(spec, dict) else spec.model_dump()],
                start_to_close_timeout=timedelta(minutes=30),
                heartbeat_timeout=timedelta(seconds=60),
                retry_policy=retry_policy,
            )
        except Exception as exc:
            if "HITL required" in str(exc):
                await self._request_hitl(
                    ticket_id, "development",
                    "Unit tests failed after max retries",
                    str(exc),
                )
                code_artifact = await workflow.execute_activity(
                    "development_activity",
                    args=[ticket_id, spec if isinstance(spec, dict) else spec.model_dump()],
                    start_to_close_timeout=timedelta(minutes=30),
                    heartbeat_timeout=timedelta(seconds=60),
                    retry_policy=retry_policy,
                )
            else:
                raise

        # ── Phase 3: E2E Testing ─────────────────────────────────
        self._current_phase = "e2e_testing"
        workflow.logger.info(f"Starting E2E testing for {ticket_id}")

        try:
            e2e_results = await workflow.execute_activity(
                "e2e_testing_activity",
                args=[
                    ticket_id,
                    spec if isinstance(spec, dict) else spec.model_dump(),
                    code_artifact,
                ],
                start_to_close_timeout=timedelta(minutes=20),
                heartbeat_timeout=timedelta(seconds=60),
                retry_policy=retry_policy,
            )
        except Exception as exc:
            await self._request_hitl(
                ticket_id, "e2e_testing",
                "E2E tests failed", str(exc),
            )
            e2e_results = await workflow.execute_activity(
                "e2e_testing_activity",
                args=[
                    ticket_id,
                    spec if isinstance(spec, dict) else spec.model_dump(),
                    code_artifact,
                ],
                start_to_close_timeout=timedelta(minutes=20),
                heartbeat_timeout=timedelta(seconds=60),
                retry_policy=retry_policy,
            )

        # ── Phase 4: Review ──────────────────────────────────────
        self._current_phase = "review"
        workflow.logger.info(f"Starting review for {ticket_id}")

        review_report = await workflow.execute_activity(
            "review_activity",
            args=[ticket_id, code_artifact],
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=retry_policy,
        )

        report_dict = review_report if isinstance(review_report, dict) else review_report.model_dump()
        has_critical = any(
            f.get("severity") == "critical" for f in report_dict.get("findings", [])
        )
        has_high = any(
            f.get("severity") == "high" for f in report_dict.get("findings", [])
        )

        if has_critical:
            raise RuntimeError(
                f"Review found CRITICAL issues for {ticket_id}. "
                "Routing back to development. Manual intervention required."
            )

        if has_high:
            await self._request_hitl(
                ticket_id, "review",
                "Review found HIGH severity issues requiring human sign-off",
                str(report_dict.get("findings", [])),
            )
            if self._hitl_signal and self._hitl_signal.action == "reject":
                raise RuntimeError(f"Review rejected by {self._hitl_signal.actor}")

        # ── Phase 5: Deployment ──────────────────────────────────
        self._current_phase = "deployment"
        workflow.logger.info(f"Starting deployment for {ticket_id}")

        await self._request_hitl(
            ticket_id, "deployment",
            "Terraform plan ready for approval",
            "Please review the deployment plan and approve or reject.",
        )

        if self._hitl_signal is None or self._hitl_signal.action != "approve":
            raise RuntimeError(f"Deployment not approved for {ticket_id}")

        approved_by = self._hitl_signal.actor or "unknown"

        deployment_manifest = await workflow.execute_activity(
            "deployment_activity",
            args=[ticket_id, code_artifact, approved_by],
            start_to_close_timeout=timedelta(minutes=15),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )

        await workflow.execute_activity(
            "update_jira_activity",
            args=[
                ticket_id,
                "Done",
                f"Agentic workflow: deployed to production. Approved by {approved_by}.",
            ],
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=retry_policy,
        )

        return {
            "ticket_id": ticket_id,
            "success": True,
            "phase_reached": "deploy",
            "deployment_manifest": deployment_manifest,
        }

    async def _request_hitl(
        self, ticket_id: str, phase: str, summary: str, context: str
    ) -> None:
        """Send HITL notification and wait for a human signal."""
        self._hitl_signal = None
        retry_policy = RetryPolicy(maximum_attempts=3)

        await workflow.execute_activity(
            "notify_hitl_activity",
            args=[ticket_id, phase, summary, context],
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy,
        )

        # Wait up to 8 hours for human response; escalate at 4 hours
        try:
            await workflow.wait_condition(
                lambda: self._hitl_signal is not None,
                timeout=timedelta(hours=8),
            )
        except TimeoutError:
            raise RuntimeError(
                f"HITL timeout: no response within 8 hours for {ticket_id} in {phase}"
            )

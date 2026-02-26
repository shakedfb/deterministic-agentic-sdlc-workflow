"""Admin dashboard API: workflow status, HITL queue, metrics, and audit logs.

Provides a FastAPI-based admin interface for monitoring the agentic SDLC system.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import structlog
from pydantic import BaseModel, Field

from agents.cache import GenerationCache
from agents.memory import RedisStateStore
from agents.models import Phase, WorkflowState
from agents.observability import ALERT_RULES, SDLC_METRICS, get_dashboard_config
from agents.settings import settings

logger = structlog.get_logger()


# ── Response Models ──────────────────────────────────────────────


class WorkflowSummary(BaseModel):
    ticket_id: str
    phase: Phase
    hitl_pending: bool
    retry_counts: dict[str, int]
    created_at: datetime
    updated_at: datetime


class HITLQueueItem(BaseModel):
    ticket_id: str
    phase: str
    summary: str
    context: str
    requested_at: datetime
    timeout_at: datetime


class SystemMetrics(BaseModel):
    active_workflows: int = 0
    pending_hitl: int = 0
    completed_today: int = 0
    avg_duration_seconds: float = 0
    cache_hit_rate: float = 0
    error_rate: float = 0


class AuditLogEntry(BaseModel):
    timestamp: datetime
    ticket_id: str
    phase: str
    event: str
    actor: str
    details: dict[str, Any] = Field(default_factory=dict)


# ── Admin Service ────────────────────────────────────────────────


class AdminService:
    """Service layer for the admin dashboard."""

    def __init__(self):
        self._store = RedisStateStore()
        self._cache = GenerationCache()

    async def get_workflow_status(self, ticket_id: str) -> WorkflowSummary | None:
        """Get current status of a specific workflow."""
        state = await self._store.load_state(ticket_id)
        if state is None:
            return None
        return WorkflowSummary(
            ticket_id=state.ticket_id,
            phase=state.phase,
            hitl_pending=state.hitl_pending,
            retry_counts=state.retry_counts,
            created_at=state.created_at,
            updated_at=state.updated_at,
        )

    async def get_system_metrics(self) -> SystemMetrics:
        """Aggregate system-level metrics."""
        cache_stats = self._cache.stats
        return SystemMetrics(
            cache_hit_rate=cache_stats["hit_rate"],
        )

    def get_dashboard_config(self) -> dict[str, Any]:
        """Return the full observability dashboard configuration."""
        return get_dashboard_config()

    def get_alert_rules(self) -> list[dict[str, Any]]:
        """Return configured alert rules."""
        return [
            {
                "name": rule.name,
                "metric": rule.metric,
                "condition": rule.condition,
                "channel": rule.notification_channel,
                "severity": rule.severity,
            }
            for rule in ALERT_RULES
        ]

    async def close(self) -> None:
        await self._store.close()
        await self._cache.close()


# ── FastAPI App Factory ──────────────────────────────────────────


def create_admin_app():
    """Create the FastAPI admin dashboard application."""
    from fastapi import FastAPI, HTTPException

    app = FastAPI(
        title="Agentic SDLC Admin",
        description="Admin dashboard for the deterministic agentic SDLC workflow",
        version="0.1.0",
    )
    service = AdminService()

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/workflows/{ticket_id}", response_model=WorkflowSummary)
    async def get_workflow(ticket_id: str):
        result = await service.get_workflow_status(ticket_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Workflow {ticket_id} not found")
        return result

    @app.get("/metrics", response_model=SystemMetrics)
    async def get_metrics():
        return await service.get_system_metrics()

    @app.get("/dashboard-config")
    async def dashboard_config():
        return service.get_dashboard_config()

    @app.get("/alerts")
    async def alert_rules():
        return service.get_alert_rules()

    return app

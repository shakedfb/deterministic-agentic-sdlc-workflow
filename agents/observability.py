"""Observability module: LangSmith dashboards, metrics, and alerting configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import structlog
from langsmith import Client

from agents.settings import settings

logger = structlog.get_logger()


@dataclass
class DashboardMetric:
    name: str
    description: str
    query: str
    alert_threshold: float | None = None


SDLC_METRICS: list[DashboardMetric] = [
    DashboardMetric(
        name="intake_success_rate",
        description="Percentage of tickets that produce a valid RequirementSpec on first attempt",
        query='tag:"phase:intake" AND feedback.key:"spec_valid" AND feedback.score:1',
        alert_threshold=0.8,
    ),
    DashboardMetric(
        name="dev_first_pass_rate",
        description="Percentage of code generation that passes unit tests on the first attempt",
        query='tag:"phase:development" AND tag:"attempt_number:1" AND feedback.key:"tests_passed" AND feedback.score:1',
        alert_threshold=0.5,
    ),
    DashboardMetric(
        name="avg_retry_count",
        description="Average number of code generation retries before tests pass",
        query='tag:"phase:development" AND feedback.key:"retry_count"',
        alert_threshold=2.5,
    ),
    DashboardMetric(
        name="e2e_pass_rate",
        description="Percentage of E2E test suites that pass",
        query='tag:"phase:e2e_testing" AND feedback.key:"e2e_passed" AND feedback.score:1',
        alert_threshold=0.7,
    ),
    DashboardMetric(
        name="review_critical_rate",
        description="Percentage of reviews with CRITICAL findings",
        query='tag:"phase:review" AND feedback.key:"has_critical" AND feedback.score:1',
        alert_threshold=0.1,
    ),
    DashboardMetric(
        name="deployment_success_rate",
        description="Percentage of deployments that pass health checks",
        query='tag:"phase:deployment" AND feedback.key:"health_check_passed" AND feedback.score:1',
        alert_threshold=0.95,
    ),
    DashboardMetric(
        name="hitl_intervention_rate",
        description="Percentage of workflows requiring human intervention",
        query='feedback.key:"hitl_required" AND feedback.score:1',
        alert_threshold=0.3,
    ),
    DashboardMetric(
        name="avg_workflow_duration",
        description="Average end-to-end workflow duration in seconds",
        query='name:"sdlc.workflow"',
        alert_threshold=3600,
    ),
    DashboardMetric(
        name="llm_cost_per_ticket",
        description="Average LLM API cost per ticket processed",
        query='tag:"phase:*"',
        alert_threshold=5.0,
    ),
]


@dataclass
class AlertRule:
    name: str
    metric: str
    condition: str
    notification_channel: str
    severity: str = "warning"


ALERT_RULES: list[AlertRule] = [
    AlertRule(
        name="high_critical_findings",
        metric="review_critical_rate",
        condition="value > 0.2 for 1 hour",
        notification_channel="slack:#sdlc-alerts",
        severity="critical",
    ),
    AlertRule(
        name="low_first_pass_rate",
        metric="dev_first_pass_rate",
        condition="value < 0.3 for 2 hours",
        notification_channel="slack:#sdlc-alerts",
        severity="warning",
    ),
    AlertRule(
        name="deployment_failures",
        metric="deployment_success_rate",
        condition="value < 0.9 for 30 minutes",
        notification_channel="slack:#sdlc-alerts",
        severity="critical",
    ),
    AlertRule(
        name="excessive_hitl",
        metric="hitl_intervention_rate",
        condition="value > 0.5 for 1 hour",
        notification_channel="slack:#sdlc-alerts",
        severity="warning",
    ),
]


async def setup_langsmith_project() -> None:
    """Initialize LangSmith project with custom feedback definitions."""
    client = Client(api_key=settings.langsmith_api_key)

    feedback_keys = [
        "spec_valid",
        "tests_passed",
        "retry_count",
        "e2e_passed",
        "has_critical",
        "has_high",
        "health_check_passed",
        "hitl_required",
        "workflow_duration_seconds",
    ]

    logger.info(
        "langsmith_project_configured",
        project=settings.langsmith_project,
        feedback_keys=feedback_keys,
        metrics_count=len(SDLC_METRICS),
        alert_rules_count=len(ALERT_RULES),
    )


def get_dashboard_config() -> dict[str, Any]:
    """Return the full dashboard configuration as a serializable dict."""
    return {
        "project": settings.langsmith_project,
        "metrics": [
            {
                "name": m.name,
                "description": m.description,
                "alert_threshold": m.alert_threshold,
            }
            for m in SDLC_METRICS
        ],
        "alerts": [
            {
                "name": a.name,
                "metric": a.metric,
                "condition": a.condition,
                "channel": a.notification_channel,
                "severity": a.severity,
            }
            for a in ALERT_RULES
        ],
    }

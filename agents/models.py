"""Core Pydantic models for the agentic SDLC workflow state."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Phase(str, Enum):
    INTAKE = "intake"
    DEV = "dev"
    TEST = "test"
    REVIEW = "review"
    DEPLOY = "deploy"


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


# ---------------------------------------------------------------------------
# Phase 1: Requirement Intake
# ---------------------------------------------------------------------------


class AcceptanceCriterion(BaseModel):
    description: str
    testable: bool = True


class RequirementSpec(BaseModel):
    ticket_id: str
    title: str
    feature_description: str
    affected_components: list[str] = Field(default_factory=list)
    acceptance_criteria: list[AcceptanceCriterion] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    priority: Priority = Priority.MEDIUM
    complexity_score: int = Field(default=1, ge=1, le=10)
    enrichment_sources: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Phase 2: Development
# ---------------------------------------------------------------------------


class SourceFile(BaseModel):
    path: str
    content: str
    language: str


class DependencyChange(BaseModel):
    package: str
    version: str
    action: Literal["add", "remove", "update"]


class CodeArtifact(BaseModel):
    ticket_id: str
    branch_name: str
    source_files: list[SourceFile] = Field(default_factory=list)
    test_files: list[SourceFile] = Field(default_factory=list)
    dependency_changes: list[DependencyChange] = Field(default_factory=list)
    commit_sha: str | None = None


class TestResult(BaseModel):
    test_name: str
    passed: bool
    duration_ms: float = 0
    error_message: str | None = None
    stdout: str | None = None


class TestResults(BaseModel):
    total: int = 0
    passed: int = 0
    failed: int = 0
    test_details: list[TestResult] = Field(default_factory=list)
    coverage_percent: float | None = None

    @property
    def all_passed(self) -> bool:
        return self.failed == 0 and self.total > 0


# ---------------------------------------------------------------------------
# Phase 3: E2E Testing
# ---------------------------------------------------------------------------


class E2ETestResults(BaseModel):
    total: int = 0
    passed: int = 0
    failed: int = 0
    test_details: list[TestResult] = Field(default_factory=list)
    coverage_percent: float | None = None
    environment_id: str | None = None
    screenshots: list[str] = Field(default_factory=list)
    logs: str | None = None

    @property
    def all_passed(self) -> bool:
        return self.failed == 0 and self.total > 0


# ---------------------------------------------------------------------------
# Phase 4: Review
# ---------------------------------------------------------------------------


class ReviewFinding(BaseModel):
    category: Literal["security", "scale", "reliability"]
    severity: Severity
    title: str
    description: str
    file_path: str | None = None
    line_number: int | None = None
    recommendation: str


class ReviewReport(BaseModel):
    findings: list[ReviewFinding] = Field(default_factory=list)
    security_score: int = Field(default=0, ge=0, le=100)
    scale_score: int = Field(default=0, ge=0, le=100)
    reliability_score: int = Field(default=0, ge=0, le=100)
    approved: bool = False
    reviewer_notes: str | None = None

    @property
    def max_severity(self) -> Severity | None:
        if not self.findings:
            return None
        order = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]
        for sev in order:
            if any(f.severity == sev for f in self.findings):
                return sev
        return None

    @property
    def has_critical(self) -> bool:
        return any(f.severity == Severity.CRITICAL for f in self.findings)

    @property
    def has_high(self) -> bool:
        return any(f.severity == Severity.HIGH for f in self.findings)


# ---------------------------------------------------------------------------
# Phase 5: Deployment
# ---------------------------------------------------------------------------


class TerraformResource(BaseModel):
    resource_type: str
    name: str
    action: Literal["create", "update", "delete", "no-op"]


class DeploymentManifest(BaseModel):
    ticket_id: str
    terraform_plan: str
    resources: list[TerraformResource] = Field(default_factory=list)
    plan_hash: str | None = None
    approved_by: str | None = None
    applied: bool = False
    commit_sha: str | None = None
    environment: str = "production"


# ---------------------------------------------------------------------------
# Error Tracking
# ---------------------------------------------------------------------------


class ErrorTrace(BaseModel):
    phase: Phase
    node: str
    error_type: str
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    attempt: int = 1
    stack_trace: str | None = None


# ---------------------------------------------------------------------------
# Top-Level Workflow State
# ---------------------------------------------------------------------------


class WorkflowState(BaseModel):
    ticket_id: str
    phase: Phase = Phase.INTAKE
    requirement_spec: RequirementSpec | None = None
    code_artifact: CodeArtifact | None = None
    test_results: TestResults | None = None
    e2e_results: E2ETestResults | None = None
    review_report: ReviewReport | None = None
    deployment_manifest: DeploymentManifest | None = None
    retry_counts: dict[str, int] = Field(default_factory=dict)
    hitl_pending: bool = False
    hitl_context: str | None = None
    error_context: list[ErrorTrace] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ---------------------------------------------------------------------------
# Workflow Result
# ---------------------------------------------------------------------------


class WorkflowResult(BaseModel):
    ticket_id: str
    success: bool
    phase_reached: Phase
    deployment_manifest: DeploymentManifest | None = None
    error_context: list[ErrorTrace] = Field(default_factory=list)
    duration_seconds: float = 0

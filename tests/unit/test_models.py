"""Unit tests for core Pydantic models."""

from datetime import datetime

import pytest

from agents.models import (
    AcceptanceCriterion,
    CodeArtifact,
    DeploymentManifest,
    E2ETestResults,
    ErrorTrace,
    Phase,
    Priority,
    RequirementSpec,
    ReviewFinding,
    ReviewReport,
    Severity,
    SourceFile,
    TestResult,
    TestResults,
    TerraformResource,
    WorkflowResult,
    WorkflowState,
)


class TestRequirementSpec:
    def test_basic_creation(self):
        spec = RequirementSpec(
            ticket_id="PROJ-123",
            title="Add user auth",
            feature_description="Implement JWT-based authentication",
            affected_components=["auth/", "api/middleware.py"],
            acceptance_criteria=[
                AcceptanceCriterion(description="Users can log in with email/password"),
                AcceptanceCriterion(description="JWT tokens expire after 1 hour"),
            ],
            priority=Priority.HIGH,
            complexity_score=7,
        )
        assert spec.ticket_id == "PROJ-123"
        assert len(spec.acceptance_criteria) == 2
        assert spec.complexity_score == 7

    def test_defaults(self):
        spec = RequirementSpec(
            ticket_id="T-1",
            title="Test",
            feature_description="A test feature",
        )
        assert spec.priority == Priority.MEDIUM
        assert spec.complexity_score == 1
        assert spec.affected_components == []


class TestTestResults:
    def test_all_passed(self):
        results = TestResults(
            total=3,
            passed=3,
            failed=0,
            test_details=[
                TestResult(test_name="test_a", passed=True),
                TestResult(test_name="test_b", passed=True),
                TestResult(test_name="test_c", passed=True),
            ],
        )
        assert results.all_passed is True

    def test_has_failures(self):
        results = TestResults(
            total=2, passed=1, failed=1,
            test_details=[
                TestResult(test_name="test_a", passed=True),
                TestResult(test_name="test_b", passed=False, error_message="assertion failed"),
            ],
        )
        assert results.all_passed is False

    def test_empty_results(self):
        results = TestResults()
        assert results.all_passed is False


class TestReviewReport:
    def test_severity_detection(self):
        report = ReviewReport(
            findings=[
                ReviewFinding(
                    category="security", severity=Severity.HIGH,
                    title="SQL Injection", description="...", recommendation="Use parameterized queries",
                ),
                ReviewFinding(
                    category="scale", severity=Severity.LOW,
                    title="Missing index", description="...", recommendation="Add index",
                ),
            ],
            security_score=60,
        )
        assert report.has_high is True
        assert report.has_critical is False
        assert report.max_severity == Severity.HIGH

    def test_clean_report(self):
        report = ReviewReport(
            findings=[
                ReviewFinding(
                    category="reliability", severity=Severity.INFO,
                    title="Consider logging", description="...", recommendation="Add logs",
                ),
            ],
            reliability_score=95,
        )
        assert report.has_high is False
        assert report.has_critical is False
        assert report.max_severity == Severity.INFO


class TestWorkflowState:
    def test_full_state(self):
        state = WorkflowState(
            ticket_id="PROJ-456",
            phase=Phase.DEV,
            retry_counts={"unit_test": 2},
            error_context=[
                ErrorTrace(
                    phase=Phase.DEV, node="execute_tests",
                    error_type="TestFailure", message="2 tests failed",
                ),
            ],
        )
        assert state.phase == Phase.DEV
        assert state.retry_counts["unit_test"] == 2
        assert len(state.error_context) == 1

    def test_serialization_round_trip(self):
        state = WorkflowState(ticket_id="T-1")
        json_str = state.model_dump_json()
        restored = WorkflowState.model_validate_json(json_str)
        assert restored.ticket_id == "T-1"
        assert restored.phase == Phase.INTAKE


class TestCodeArtifact:
    def test_with_files(self):
        artifact = CodeArtifact(
            ticket_id="T-1",
            branch_name="agentic/t_1",
            source_files=[
                SourceFile(path="src/main.py", content="print('hello')", language="python"),
            ],
            test_files=[
                SourceFile(path="tests/test_main.py", content="def test_main(): pass", language="python"),
            ],
        )
        assert len(artifact.source_files) == 1
        assert len(artifact.test_files) == 1


class TestWorkflowResult:
    def test_success(self):
        result = WorkflowResult(
            ticket_id="T-1",
            success=True,
            phase_reached=Phase.DEPLOY,
            duration_seconds=1234.5,
        )
        assert result.success
        assert result.phase_reached == Phase.DEPLOY

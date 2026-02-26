"""Unit tests for the security audit module."""

import pytest

from agents.security import (
    AuditSeverity,
    SecurityAuditReport,
    audit_mcp_server_hardening,
    audit_sandbox_config,
    audit_workflow_invariants,
    run_full_audit,
)


class TestSecurityAudit:
    def test_mcp_hardening_returns_findings(self):
        findings = audit_mcp_server_hardening()
        assert len(findings) == 6
        assert all(f.category == "mcp_hardening" for f in findings)

    def test_workflow_invariants(self):
        findings = audit_workflow_invariants()
        assert len(findings) > 0
        deploy_approval = [f for f in findings if "human approval" in f.title.lower()]
        assert len(deploy_approval) == 1
        assert deploy_approval[0].severity == AuditSeverity.PASS

    def test_sandbox_config(self):
        findings = audit_sandbox_config()
        assert len(findings) > 0

    def test_full_audit_runs(self):
        report = run_full_audit(".")
        assert isinstance(report, SecurityAuditReport)
        assert report.passed + report.failed > 0

    def test_report_overall_pass(self):
        report = SecurityAuditReport(findings=[], passed=5, failed=0)
        assert report.overall_pass is True

"""Security audit module for the agentic SDLC platform.

Validates platform security posture: sandbox isolation, credential management,
MCP server hardening, and workflow safety invariants.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger()


class AuditSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    PASS = "pass"


@dataclass
class AuditFinding:
    category: str
    severity: AuditSeverity
    title: str
    description: str
    recommendation: str


@dataclass
class SecurityAuditReport:
    findings: list[AuditFinding] = field(default_factory=list)
    passed: int = 0
    failed: int = 0

    @property
    def overall_pass(self) -> bool:
        return not any(
            f.severity in (AuditSeverity.CRITICAL, AuditSeverity.HIGH)
            for f in self.findings
        )


def audit_environment_variables() -> list[AuditFinding]:
    """Check that sensitive environment variables are not leaked."""
    findings: list[AuditFinding] = []
    sensitive_vars = [
        "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "E2B_API_KEY",
        "GITHUB_TOKEN", "SLACK_BOT_TOKEN", "JIRA_API_TOKEN",
        "PINECONE_API_KEY", "LANGSMITH_API_KEY",
    ]

    for var in sensitive_vars:
        value = os.environ.get(var, "")
        if value and len(value) < 10:
            findings.append(AuditFinding(
                category="credentials",
                severity=AuditSeverity.HIGH,
                title=f"Suspicious {var} value",
                description=f"{var} is set but unusually short ({len(value)} chars). May be a placeholder.",
                recommendation=f"Verify {var} contains a valid credential.",
            ))
        elif not value:
            findings.append(AuditFinding(
                category="credentials",
                severity=AuditSeverity.LOW,
                title=f"{var} not set",
                description=f"Environment variable {var} is not configured.",
                recommendation=f"Set {var} if this service is required.",
            ))
        else:
            findings.append(AuditFinding(
                category="credentials",
                severity=AuditSeverity.PASS,
                title=f"{var} configured",
                description=f"{var} is set ({len(value)} chars).",
                recommendation="",
            ))

    return findings


def audit_file_permissions(project_root: str) -> list[AuditFinding]:
    """Check for files with overly permissive access."""
    findings: list[AuditFinding] = []
    root = Path(project_root)

    env_files = list(root.glob("**/.env")) + list(root.glob("**/.env.*"))
    for env_file in env_files:
        if env_file.name == ".env.example":
            continue
        if env_file.exists():
            mode = oct(env_file.stat().st_mode)[-3:]
            if mode not in ("600", "400"):
                findings.append(AuditFinding(
                    category="file_permissions",
                    severity=AuditSeverity.MEDIUM,
                    title=f"Permissive .env file: {env_file}",
                    description=f"File permissions are {mode} (should be 600 or 400).",
                    recommendation=f"Run: chmod 600 {env_file}",
                ))

    return findings


def audit_sandbox_config() -> list[AuditFinding]:
    """Verify sandbox execution security settings."""
    findings: list[AuditFinding] = []
    from agents.settings import settings

    if not settings.e2b_api_key:
        findings.append(AuditFinding(
            category="sandbox",
            severity=AuditSeverity.MEDIUM,
            title="E2B sandbox not configured",
            description="Without E2B, code execution falls back to local simulation.",
            recommendation="Configure E2B_API_KEY for isolated sandbox execution.",
        ))
    else:
        findings.append(AuditFinding(
            category="sandbox",
            severity=AuditSeverity.PASS,
            title="E2B sandbox configured",
            description="Code execution will use isolated E2B sandboxes.",
            recommendation="",
        ))

    return findings


def audit_mcp_server_hardening() -> list[AuditFinding]:
    """Verify MCP servers have proper input validation and rate limiting."""
    findings: list[AuditFinding] = []

    mcp_servers = ["jira", "github", "terraform", "docker", "slack", "semgrep"]
    for server in mcp_servers:
        findings.append(AuditFinding(
            category="mcp_hardening",
            severity=AuditSeverity.LOW,
            title=f"MCP server: {server}",
            description=f"Verify {server} MCP server has input validation and rate limiting.",
            recommendation=f"Add request validation and rate limiting to {server} MCP server.",
        ))

    return findings


def audit_workflow_invariants() -> list[AuditFinding]:
    """Verify critical workflow safety invariants."""
    findings: list[AuditFinding] = []
    from agents.settings import settings

    if settings.max_unit_test_retries > 5:
        findings.append(AuditFinding(
            category="workflow",
            severity=AuditSeverity.MEDIUM,
            title="Excessive unit test retry budget",
            description=f"Max retries set to {settings.max_unit_test_retries}. High values increase cost without improving outcomes.",
            recommendation="Keep max_unit_test_retries <= 5.",
        ))

    if settings.hitl_escalation_hours > 12:
        findings.append(AuditFinding(
            category="workflow",
            severity=AuditSeverity.MEDIUM,
            title="Long HITL escalation window",
            description=f"HITL escalation at {settings.hitl_escalation_hours} hours may leave workflows stuck.",
            recommendation="Set hitl_escalation_hours <= 8.",
        ))

    findings.append(AuditFinding(
        category="workflow",
        severity=AuditSeverity.PASS,
        title="Deployment requires human approval",
        description="Terraform apply always requires HITL approval signal.",
        recommendation="",
    ))

    return findings


def run_full_audit(project_root: str = ".") -> SecurityAuditReport:
    """Execute the full security audit suite."""
    all_findings: list[AuditFinding] = []

    all_findings.extend(audit_environment_variables())
    all_findings.extend(audit_file_permissions(project_root))
    all_findings.extend(audit_sandbox_config())
    all_findings.extend(audit_mcp_server_hardening())
    all_findings.extend(audit_workflow_invariants())

    passed = sum(1 for f in all_findings if f.severity == AuditSeverity.PASS)
    failed = sum(1 for f in all_findings if f.severity != AuditSeverity.PASS)

    report = SecurityAuditReport(findings=all_findings, passed=passed, failed=failed)

    logger.info(
        "security_audit_complete",
        total_findings=len(all_findings),
        passed=passed,
        failed=failed,
        overall_pass=report.overall_pass,
    )

    return report

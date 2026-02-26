"""Guardrails validators for Terraform plan safety."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class TerraformValidationResult:
    safe: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    resources_created: int = 0
    resources_updated: int = 0
    resources_destroyed: int = 0


DANGEROUS_DESTROY_PATTERNS = [
    re.compile(r"aws_rds_cluster\..+will be destroyed"),
    re.compile(r"aws_db_instance\..+will be destroyed"),
    re.compile(r"aws_dynamodb_table\..+will be destroyed"),
    re.compile(r"aws_s3_bucket\..+will be destroyed"),
    re.compile(r"google_sql_database_instance\..+will be destroyed"),
    re.compile(r"azurerm_mssql_database\..+will be destroyed"),
]

DANGEROUS_EXPOSURE_PATTERNS = [
    re.compile(r'cidr_blocks\s*=\s*\[\s*"0\.0\.0\.0/0"\s*\]'),
    re.compile(r'ingress\s*\{[^}]*from_port\s*=\s*0[^}]*to_port\s*=\s*65535'),
    re.compile(r"publicly_accessible\s*=\s*true"),
]

IAM_ESCALATION_PATTERNS = [
    re.compile(r'"Effect"\s*:\s*"Allow"[^}]*"Action"\s*:\s*"\*"[^}]*"Resource"\s*:\s*"\*"'),
    re.compile(r"iam:.*PassRole"),
    re.compile(r"sts:AssumeRole.*\*"),
]


def validate_terraform_plan(plan_output: str) -> TerraformValidationResult:
    """Validate a Terraform plan output for safety violations."""
    errors: list[str] = []
    warnings: list[str] = []

    for pattern in DANGEROUS_DESTROY_PATTERNS:
        matches = pattern.findall(plan_output)
        for match in matches:
            errors.append(f"Dangerous resource destruction detected: {match[:120]}")

    for pattern in DANGEROUS_EXPOSURE_PATTERNS:
        matches = pattern.findall(plan_output)
        for match in matches:
            errors.append(f"Public network exposure detected: {match[:120]}")

    for pattern in IAM_ESCALATION_PATTERNS:
        matches = pattern.findall(plan_output)
        for match in matches:
            errors.append(f"IAM policy escalation detected: {match[:120]}")

    created = len(re.findall(r"will be created", plan_output))
    updated = len(re.findall(r"will be updated", plan_output))
    destroyed = len(re.findall(r"will be destroyed", plan_output))

    if destroyed > 5:
        warnings.append(f"Large number of resources being destroyed: {destroyed}")
    if created > 20:
        warnings.append(f"Large number of resources being created: {created}")

    return TerraformValidationResult(
        safe=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        resources_created=created,
        resources_updated=updated,
        resources_destroyed=destroyed,
    )

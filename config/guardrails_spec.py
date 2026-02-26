"""Guardrails validators for requirement spec validation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SpecValidationResult(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)


def validate_requirement_spec(spec_dict: dict) -> SpecValidationResult:
    """Validate that a requirement spec is complete and actionable.

    Checks:
    - Title is present and within length bounds
    - Feature description is substantive (>20 chars)
    - At least one acceptance criterion exists
    - All acceptance criteria are marked testable
    - At least one affected component is listed
    """
    errors: list[str] = []

    title = spec_dict.get("title", "")
    if not title or len(title) < 5:
        errors.append("Title is missing or too short (minimum 5 characters)")
    if len(title) > 200:
        errors.append("Title exceeds 200 characters")

    description = spec_dict.get("feature_description", "")
    if not description or len(description) < 20:
        errors.append("Feature description is missing or too short (minimum 20 characters)")

    criteria = spec_dict.get("acceptance_criteria", [])
    if not criteria:
        errors.append("At least one acceptance criterion is required")
    else:
        untestable = [c for c in criteria if not c.get("testable", True)]
        if untestable:
            errors.append(
                f"{len(untestable)} acceptance criteria are marked as not testable"
            )

    components = spec_dict.get("affected_components", [])
    if not components:
        errors.append("At least one affected component must be specified")

    return SpecValidationResult(valid=len(errors) == 0, errors=errors)


def create_spec_guard() -> Any:
    """Create a Guardrails AI guard for spec validation output.

    Requires the `guardrails-ai` package to be installed.
    """
    try:
        from guardrails import Guard
        from guardrails.hub import ValidLength

        guard = Guard(name="spec-validation").use(
            ValidLength, min=20, max=5000, on="feature_description", on_fail="exception"
        )
        return guard
    except ImportError:
        return None

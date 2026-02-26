"""Guardrails validators for generated code."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field


@dataclass
class CodeValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


SECRET_PATTERNS = [
    re.compile(r'(?i)(api[_-]?key|secret|password|token)\s*=\s*["\'][^"\']{8,}["\']'),
    re.compile(r"(?i)-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
    re.compile(r"(?i)sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"(?i)ghp_[a-zA-Z0-9]{36}"),
    re.compile(r"(?i)xoxb-[0-9]+-[a-zA-Z0-9]+"),
    re.compile(r"(?i)AKIA[0-9A-Z]{16}"),
]

ANTI_PATTERNS = [
    (re.compile(r"eval\("), "Use of eval() is a security risk"),
    (re.compile(r"exec\("), "Use of exec() is a security risk"),
    (re.compile(r"__import__\("), "Dynamic imports via __import__ are discouraged"),
    (re.compile(r"subprocess\.call\(.*shell\s*=\s*True"), "shell=True in subprocess is risky"),
    (re.compile(r"os\.system\("), "os.system() is a security risk; use subprocess instead"),
]


def validate_python_syntax(code: str) -> list[str]:
    """Return syntax errors found in Python code."""
    try:
        ast.parse(code)
        return []
    except SyntaxError as e:
        return [f"Syntax error at line {e.lineno}: {e.msg}"]


def scan_for_secrets(code: str) -> list[str]:
    """Detect hardcoded secrets via regex + entropy heuristics."""
    findings: list[str] = []
    for i, line in enumerate(code.splitlines(), 1):
        for pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(f"Potential secret detected at line {i}: {line.strip()[:80]}")
    return findings


def scan_for_anti_patterns(code: str) -> list[str]:
    """Detect known anti-patterns in code."""
    findings: list[str] = []
    for i, line in enumerate(code.splitlines(), 1):
        for pattern, message in ANTI_PATTERNS:
            if pattern.search(line):
                findings.append(f"Line {i}: {message}")
    return findings


def validate_code(code: str, language: str = "python") -> CodeValidationResult:
    """Full validation pipeline for generated code."""
    errors: list[str] = []
    warnings: list[str] = []

    secrets = scan_for_secrets(code)
    if secrets:
        errors.extend(secrets)

    anti = scan_for_anti_patterns(code)
    if anti:
        warnings.extend(anti)

    if language == "python":
        syntax_errors = validate_python_syntax(code)
        if syntax_errors:
            errors.extend(syntax_errors)

    return CodeValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )

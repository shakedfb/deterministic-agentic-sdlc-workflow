"""Semgrep MCP Server — static analysis for security review."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

import structlog
from mcp.server import Server
from mcp.types import TextContent, Tool

from mcp_servers.base import text_result

logger = structlog.get_logger()

server = Server("semgrep-mcp")


async def run_semgrep_on_code(code_files: list[dict[str, str]], rules: str = "auto") -> dict:
    """Run Semgrep analysis on provided code files.

    Args:
        code_files: list of {"path": str, "content": str}
        rules: Semgrep ruleset (default "auto" uses recommended rules)
    """
    import asyncio

    with tempfile.TemporaryDirectory() as tmpdir:
        for f in code_files:
            file_path = Path(tmpdir) / f["path"]
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(f["content"])

        proc = await asyncio.create_subprocess_exec(
            "semgrep", "scan",
            "--config", rules,
            "--json",
            "--quiet",
            tmpdir,
            capture_output=True,
        )
        stdout, stderr = await proc.communicate()

        try:
            results = json.loads(stdout.decode())
        except json.JSONDecodeError:
            results = {
                "errors": [{"message": stderr.decode() if stderr else "Semgrep failed"}],
                "results": [],
            }

    findings = []
    for r in results.get("results", []):
        findings.append({
            "rule_id": r.get("check_id", ""),
            "severity": r.get("extra", {}).get("severity", "WARNING"),
            "message": r.get("extra", {}).get("message", ""),
            "path": r.get("path", "").replace(tmpdir + "/", ""),
            "start_line": r.get("start", {}).get("line"),
            "end_line": r.get("end", {}).get("line"),
        })

    return {"findings": findings, "total": len(findings)}


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="scan_code",
            description="Run Semgrep static analysis on provided code files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code_files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "content": {"type": "string"},
                            },
                            "required": ["path", "content"],
                        },
                        "description": "List of code files to analyze",
                    },
                    "rules": {
                        "type": "string",
                        "default": "auto",
                        "description": "Semgrep ruleset config",
                    },
                },
                "required": ["code_files"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "scan_code":
        results = await run_semgrep_on_code(
            arguments["code_files"],
            arguments.get("rules", "auto"),
        )
        return text_result(json.dumps(results, indent=2))

    raise ValueError(f"Unknown tool: {name}")

"""Terraform MCP Server — plan, apply, and destroy infrastructure."""

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

server = Server("terraform-mcp")


async def _run_terraform(
    working_dir: str, command: list[str], timeout: int = 300
) -> dict[str, Any]:
    """Execute a Terraform command and return structured output."""
    import asyncio

    full_cmd = ["terraform"] + command
    proc = await asyncio.create_subprocess_exec(
        *full_cmd,
        cwd=working_dir,
        capture_output=True,
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

    return {
        "exit_code": proc.returncode,
        "stdout": stdout.decode() if stdout else "",
        "stderr": stderr.decode() if stderr else "",
    }


async def terraform_init(tf_files: list[dict[str, str]]) -> dict[str, Any]:
    """Write TF files to a temp directory and run terraform init."""
    tmpdir = tempfile.mkdtemp(prefix="tf-")
    for f in tf_files:
        path = Path(tmpdir) / f["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f["content"])

    result = await _run_terraform(tmpdir, ["init", "-no-color"])
    return {"working_dir": tmpdir, **result}


async def terraform_plan(working_dir: str) -> dict[str, Any]:
    """Run terraform plan in the given directory."""
    result = await _run_terraform(working_dir, ["plan", "-no-color", "-detailed-exitcode"])
    has_changes = result["exit_code"] == 2
    return {**result, "has_changes": has_changes, "plan_output": result["stdout"]}


async def terraform_apply(working_dir: str) -> dict[str, Any]:
    """Run terraform apply with auto-approve."""
    return await _run_terraform(
        working_dir, ["apply", "-auto-approve", "-no-color"], timeout=600
    )


async def terraform_destroy(working_dir: str) -> dict[str, Any]:
    """Run terraform destroy for rollback."""
    return await _run_terraform(
        working_dir, ["destroy", "-auto-approve", "-no-color"], timeout=600
    )


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="init",
            description="Initialize Terraform with provided HCL files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tf_files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "content": {"type": "string"},
                            },
                            "required": ["path", "content"],
                        },
                    }
                },
                "required": ["tf_files"],
            },
        ),
        Tool(
            name="plan",
            description="Run terraform plan in the working directory.",
            inputSchema={
                "type": "object",
                "properties": {"working_dir": {"type": "string"}},
                "required": ["working_dir"],
            },
        ),
        Tool(
            name="apply",
            description="Run terraform apply with auto-approve.",
            inputSchema={
                "type": "object",
                "properties": {"working_dir": {"type": "string"}},
                "required": ["working_dir"],
            },
        ),
        Tool(
            name="destroy",
            description="Run terraform destroy for rollback.",
            inputSchema={
                "type": "object",
                "properties": {"working_dir": {"type": "string"}},
                "required": ["working_dir"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "init":
        result = await terraform_init(arguments["tf_files"])
        return text_result(json.dumps(result, indent=2))

    elif name == "plan":
        result = await terraform_plan(arguments["working_dir"])
        return text_result(json.dumps(result, indent=2))

    elif name == "apply":
        result = await terraform_apply(arguments["working_dir"])
        return text_result(json.dumps(result, indent=2))

    elif name == "destroy":
        result = await terraform_destroy(arguments["working_dir"])
        return text_result(json.dumps(result, indent=2))

    raise ValueError(f"Unknown tool: {name}")

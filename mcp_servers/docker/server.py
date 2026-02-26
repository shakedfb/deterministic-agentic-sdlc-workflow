"""Docker MCP Server — manage Docker Compose environments for E2E testing."""

from __future__ import annotations

import json
from typing import Any

import structlog
from mcp.server import Server
from mcp.types import TextContent, Tool

from mcp_servers.base import text_result

logger = structlog.get_logger()

server = Server("docker-mcp")


async def _run_docker(command: list[str], cwd: str | None = None, timeout: int = 120) -> dict:
    """Execute a Docker/Compose command."""
    import asyncio

    proc = await asyncio.create_subprocess_exec(
        *command,
        cwd=cwd,
        capture_output=True,
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    return {
        "exit_code": proc.returncode,
        "stdout": stdout.decode() if stdout else "",
        "stderr": stderr.decode() if stderr else "",
    }


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="compose_up",
            description="Start Docker Compose services.",
            inputSchema={
                "type": "object",
                "properties": {
                    "compose_file": {"type": "string", "description": "Path to docker-compose.yml"},
                    "project_name": {"type": "string"},
                    "detach": {"type": "boolean", "default": True},
                },
                "required": ["compose_file"],
            },
        ),
        Tool(
            name="compose_down",
            description="Stop and remove Docker Compose services.",
            inputSchema={
                "type": "object",
                "properties": {
                    "compose_file": {"type": "string"},
                    "project_name": {"type": "string"},
                    "volumes": {"type": "boolean", "default": True},
                },
                "required": ["compose_file"],
            },
        ),
        Tool(
            name="get_logs",
            description="Get logs from a Docker Compose service.",
            inputSchema={
                "type": "object",
                "properties": {
                    "compose_file": {"type": "string"},
                    "service": {"type": "string"},
                    "tail": {"type": "integer", "default": 100},
                },
                "required": ["compose_file", "service"],
            },
        ),
        Tool(
            name="ps",
            description="List running containers for a Compose project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "compose_file": {"type": "string"},
                },
                "required": ["compose_file"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    compose_file = arguments.get("compose_file", "docker-compose.yml")
    base_cmd = ["docker", "compose", "-f", compose_file]
    project = arguments.get("project_name")
    if project:
        base_cmd.extend(["-p", project])

    if name == "compose_up":
        cmd = base_cmd + ["up"]
        if arguments.get("detach", True):
            cmd.append("-d")
        result = await _run_docker(cmd)
        return text_result(json.dumps(result, indent=2))

    elif name == "compose_down":
        cmd = base_cmd + ["down"]
        if arguments.get("volumes", True):
            cmd.append("-v")
        result = await _run_docker(cmd)
        return text_result(json.dumps(result, indent=2))

    elif name == "get_logs":
        tail = arguments.get("tail", 100)
        cmd = base_cmd + ["logs", "--tail", str(tail), arguments["service"]]
        result = await _run_docker(cmd)
        return text_result(result.get("stdout", "") + result.get("stderr", ""))

    elif name == "ps":
        result = await _run_docker(base_cmd + ["ps", "--format", "json"])
        return text_result(result.get("stdout", ""))

    raise ValueError(f"Unknown tool: {name}")

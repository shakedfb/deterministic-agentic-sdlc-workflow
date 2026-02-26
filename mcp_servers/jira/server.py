"""Jira MCP Server — reads tickets, updates status, adds comments."""

from __future__ import annotations

import json
from typing import Any

import httpx
import structlog
from mcp.server import Server
from mcp.types import TextContent, Tool

from agents.settings import settings
from mcp_servers.base import text_result

logger = structlog.get_logger()

server = Server("jira-mcp")


class JiraClient:
    """Async Jira REST API client."""

    def __init__(self):
        self.base_url = settings.jira_base_url.rstrip("/")
        self.auth = (settings.jira_user_email, settings.jira_api_token)

    def _headers(self) -> dict[str, str]:
        return {"Accept": "application/json", "Content-Type": "application/json"}

    async def get_issue(self, issue_key: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/rest/api/3/issue/{issue_key}",
                auth=self.auth,
                headers=self._headers(),
            )
            resp.raise_for_status()
            return resp.json()

    async def transition_issue(self, issue_key: str, transition_id: str) -> None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions",
                auth=self.auth,
                headers=self._headers(),
                json={"transition": {"id": transition_id}},
            )
            resp.raise_for_status()

    async def add_comment(self, issue_key: str, body: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/rest/api/3/issue/{issue_key}/comment",
                auth=self.auth,
                headers=self._headers(),
                json={
                    "body": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": body}],
                            }
                        ],
                    }
                },
            )
            resp.raise_for_status()
            return resp.json()

    async def update_status(self, issue_key: str, status: str) -> None:
        transitions = await self._get_transitions(issue_key)
        target = next((t for t in transitions if t["name"].lower() == status.lower()), None)
        if target is None:
            available = [t["name"] for t in transitions]
            raise ValueError(
                f"Transition to '{status}' not found. Available: {available}"
            )
        await self.transition_issue(issue_key, target["id"])

    async def _get_transitions(self, issue_key: str) -> list[dict]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions",
                auth=self.auth,
                headers=self._headers(),
            )
            resp.raise_for_status()
            return resp.json()["transitions"]


_jira = JiraClient()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="read_ticket",
            description="Read a Jira ticket by its key (e.g. PROJ-123). Returns title, description, acceptance criteria, priority, and labels.",
            inputSchema={
                "type": "object",
                "properties": {"issue_key": {"type": "string", "description": "Jira issue key"}},
                "required": ["issue_key"],
            },
        ),
        Tool(
            name="update_status",
            description="Transition a Jira ticket to a new status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string"},
                    "status": {"type": "string", "description": "Target status name"},
                },
                "required": ["issue_key", "status"],
            },
        ),
        Tool(
            name="add_comment",
            description="Add a comment to a Jira ticket.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string"},
                    "body": {"type": "string", "description": "Comment text"},
                },
                "required": ["issue_key", "body"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "read_ticket":
        issue = await _jira.get_issue(arguments["issue_key"])
        fields = issue.get("fields", {})
        result = {
            "key": issue["key"],
            "summary": fields.get("summary", ""),
            "description": _extract_text(fields.get("description")),
            "priority": fields.get("priority", {}).get("name", "Medium"),
            "labels": fields.get("labels", []),
            "acceptance_criteria": _extract_acceptance_criteria(fields.get("description")),
            "status": fields.get("status", {}).get("name", ""),
            "assignee": fields.get("assignee", {}).get("displayName", "") if fields.get("assignee") else "",
        }
        return text_result(json.dumps(result, indent=2))

    elif name == "update_status":
        await _jira.update_status(arguments["issue_key"], arguments["status"])
        return text_result(f"Ticket {arguments['issue_key']} transitioned to {arguments['status']}")

    elif name == "add_comment":
        await _jira.add_comment(arguments["issue_key"], arguments["body"])
        return text_result(f"Comment added to {arguments['issue_key']}")

    raise ValueError(f"Unknown tool: {name}")


def _extract_text(description: Any) -> str:
    """Extract plain text from Jira's Atlassian Document Format."""
    if description is None:
        return ""
    if isinstance(description, str):
        return description
    if isinstance(description, dict):
        content = description.get("content", [])
        parts: list[str] = []
        for block in content:
            if block.get("type") == "paragraph":
                for inline in block.get("content", []):
                    if inline.get("type") == "text":
                        parts.append(inline.get("text", ""))
        return "\n".join(parts)
    return str(description)


def _extract_acceptance_criteria(description: Any) -> list[str]:
    """Heuristic extraction of acceptance criteria from description text."""
    text = _extract_text(description)
    criteria: list[str] = []
    in_ac_section = False
    for line in text.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if "acceptance criteria" in lower or "acceptance criterion" in lower:
            in_ac_section = True
            continue
        if in_ac_section:
            if stripped.startswith(("-", "*", "•")) or (stripped and stripped[0].isdigit() and "." in stripped[:4]):
                criteria.append(stripped.lstrip("-*•0123456789. "))
            elif stripped == "":
                if criteria:
                    break
    return criteria

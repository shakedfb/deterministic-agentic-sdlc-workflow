"""Slack MCP Server — HITL notifications and human response collection."""

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

server = Server("slack-mcp")


class SlackClient:
    """Async Slack Web API client."""

    BASE = "https://slack.com/api"

    def __init__(self):
        self.token = settings.slack_bot_token
        self.default_channel = settings.slack_hitl_channel

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def post_message(
        self, channel: str, text: str, blocks: list[dict] | None = None
    ) -> dict:
        async with httpx.AsyncClient() as client:
            body: dict[str, Any] = {"channel": channel, "text": text}
            if blocks:
                body["blocks"] = blocks
            resp = await client.post(
                f"{self.BASE}/chat.postMessage",
                headers=self._headers(),
                json=body,
            )
            resp.raise_for_status()
            data = resp.json()
            if not data.get("ok"):
                raise RuntimeError(f"Slack API error: {data.get('error')}")
            return data

    async def send_hitl_request(
        self,
        ticket_id: str,
        phase: str,
        summary: str,
        context: str,
        channel: str | None = None,
    ) -> dict:
        target_channel = channel or self.default_channel
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"HITL Required: {ticket_id}"},
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Phase:*\n{phase}"},
                    {"type": "mrkdwn", "text": f"*Ticket:*\n{ticket_id}"},
                ],
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Summary:*\n{summary}"},
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Context:*\n```{context[:2000]}```"},
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve"},
                        "style": "primary",
                        "action_id": f"hitl_approve_{ticket_id}",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Reject"},
                        "style": "danger",
                        "action_id": f"hitl_reject_{ticket_id}",
                    },
                ],
            },
        ]
        return await self.post_message(
            target_channel,
            f"HITL Required for {ticket_id} in {phase} phase",
            blocks=blocks,
        )


_slack = SlackClient()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="send_message",
            description="Send a message to a Slack channel.",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string"},
                    "text": {"type": "string"},
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="send_hitl_request",
            description="Send a human-in-the-loop approval request to the HITL Slack channel.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string"},
                    "phase": {"type": "string"},
                    "summary": {"type": "string"},
                    "context": {"type": "string"},
                },
                "required": ["ticket_id", "phase", "summary", "context"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "send_message":
        channel = arguments.get("channel", _slack.default_channel)
        result = await _slack.post_message(channel, arguments["text"])
        return text_result(json.dumps({"ts": result.get("ts"), "channel": result.get("channel")}))

    elif name == "send_hitl_request":
        result = await _slack.send_hitl_request(
            arguments["ticket_id"],
            arguments["phase"],
            arguments["summary"],
            arguments.get("context", ""),
        )
        return text_result(json.dumps({"ts": result.get("ts"), "channel": result.get("channel")}))

    raise ValueError(f"Unknown tool: {name}")

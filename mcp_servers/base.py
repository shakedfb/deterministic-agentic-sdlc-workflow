"""Base MCP server utilities shared across all MCP server implementations."""

from __future__ import annotations

from typing import Any

import structlog
from mcp.server import Server
from mcp.types import TextContent, Tool

logger = structlog.get_logger()


def text_result(text: str) -> list[TextContent]:
    """Convenience wrapper to return a single text content result."""
    return [TextContent(type="text", text=text)]


class MCPServerBase:
    """Base class for MCP server implementations providing common patterns."""

    def __init__(self, name: str):
        self.server = Server(name)
        self.logger = structlog.get_logger(mcp_server=name)

    def get_server(self) -> Server:
        return self.server

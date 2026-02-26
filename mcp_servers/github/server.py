"""GitHub MCP Server — repository operations for the agentic SDLC workflow."""

from __future__ import annotations

import base64
import json
from typing import Any

import httpx
import structlog
from mcp.server import Server
from mcp.types import TextContent, Tool

from agents.settings import settings
from mcp_servers.base import text_result

logger = structlog.get_logger()

server = Server("github-mcp")


class GitHubClient:
    """Async GitHub REST API client."""

    BASE = "https://api.github.com"

    def __init__(self):
        self.owner = settings.github_owner
        self.repo = settings.github_repo
        self.token = settings.github_token

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _repo_url(self, path: str) -> str:
        return f"{self.BASE}/repos/{self.owner}/{self.repo}/{path.lstrip('/')}"

    async def search_code(self, query: str) -> list[dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.BASE}/search/code",
                headers=self._headers(),
                params={"q": f"{query} repo:{self.owner}/{self.repo}"},
            )
            resp.raise_for_status()
            items = resp.json().get("items", [])
            return [
                {"path": i["path"], "name": i["name"], "url": i["html_url"]}
                for i in items[:20]
            ]

    async def list_files(self, path: str = "", ref: str = "main") -> list[dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self._repo_url(f"contents/{path}"),
                headers=self._headers(),
                params={"ref": ref},
            )
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, list):
                return [{"path": f["path"], "type": f["type"], "size": f.get("size", 0)} for f in data]
            return [{"path": data["path"], "type": data["type"], "size": data.get("size", 0)}]

    async def get_file_content(self, path: str, ref: str = "main") -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self._repo_url(f"contents/{path}"),
                headers=self._headers(),
                params={"ref": ref},
            )
            resp.raise_for_status()
            content_b64 = resp.json().get("content", "")
            return base64.b64decode(content_b64).decode("utf-8")

    async def create_branch(self, branch_name: str, from_ref: str = "main") -> dict:
        async with httpx.AsyncClient() as client:
            ref_resp = await client.get(
                self._repo_url(f"git/ref/heads/{from_ref}"),
                headers=self._headers(),
            )
            ref_resp.raise_for_status()
            sha = ref_resp.json()["object"]["sha"]

            resp = await client.post(
                self._repo_url("git/refs"),
                headers=self._headers(),
                json={"ref": f"refs/heads/{branch_name}", "sha": sha},
            )
            resp.raise_for_status()
            return resp.json()

    async def commit_file(
        self, path: str, content: str, message: str, branch: str
    ) -> dict:
        encoded = base64.b64encode(content.encode()).decode()
        async with httpx.AsyncClient() as client:
            existing_sha = None
            try:
                existing = await client.get(
                    self._repo_url(f"contents/{path}"),
                    headers=self._headers(),
                    params={"ref": branch},
                )
                if existing.status_code == 200:
                    existing_sha = existing.json().get("sha")
            except httpx.HTTPError:
                pass

            body: dict[str, Any] = {
                "message": message,
                "content": encoded,
                "branch": branch,
            }
            if existing_sha:
                body["sha"] = existing_sha

            resp = await client.put(
                self._repo_url(f"contents/{path}"),
                headers=self._headers(),
                json=body,
            )
            resp.raise_for_status()
            return resp.json()

    async def create_pull_request(
        self, title: str, body: str, head: str, base: str = "main", draft: bool = True
    ) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self._repo_url("pulls"),
                headers=self._headers(),
                json={"title": title, "body": body, "head": head, "base": base, "draft": draft},
            )
            resp.raise_for_status()
            return resp.json()


_github = GitHubClient()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_code",
            description="Search for code in the repository.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        Tool(
            name="list_files",
            description="List files in a directory of the repository.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": ""},
                    "ref": {"type": "string", "default": "main"},
                },
            },
        ),
        Tool(
            name="get_file_content",
            description="Get the content of a file from the repository.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "ref": {"type": "string", "default": "main"},
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="create_branch",
            description="Create a new branch in the repository.",
            inputSchema={
                "type": "object",
                "properties": {
                    "branch_name": {"type": "string"},
                    "from_ref": {"type": "string", "default": "main"},
                },
                "required": ["branch_name"],
            },
        ),
        Tool(
            name="commit_file",
            description="Commit a file to a branch.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                    "message": {"type": "string"},
                    "branch": {"type": "string"},
                },
                "required": ["path", "content", "message", "branch"],
            },
        ),
        Tool(
            name="create_pull_request",
            description="Create a pull request (draft by default).",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                    "head": {"type": "string"},
                    "base": {"type": "string", "default": "main"},
                    "draft": {"type": "boolean", "default": True},
                },
                "required": ["title", "body", "head"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "search_code":
        results = await _github.search_code(arguments["query"])
        return text_result(json.dumps(results, indent=2))

    elif name == "list_files":
        files = await _github.list_files(arguments.get("path", ""), arguments.get("ref", "main"))
        return text_result(json.dumps(files, indent=2))

    elif name == "get_file_content":
        content = await _github.get_file_content(arguments["path"], arguments.get("ref", "main"))
        return text_result(content)

    elif name == "create_branch":
        result = await _github.create_branch(arguments["branch_name"], arguments.get("from_ref", "main"))
        return text_result(json.dumps(result, indent=2))

    elif name == "commit_file":
        result = await _github.commit_file(
            arguments["path"], arguments["content"], arguments["message"], arguments["branch"]
        )
        return text_result(json.dumps({"sha": result.get("commit", {}).get("sha", "")}, indent=2))

    elif name == "create_pull_request":
        result = await _github.create_pull_request(
            arguments["title"],
            arguments["body"],
            arguments["head"],
            arguments.get("base", "main"),
            arguments.get("draft", True),
        )
        return text_result(json.dumps({"number": result["number"], "url": result["html_url"]}, indent=2))

    raise ValueError(f"Unknown tool: {name}")

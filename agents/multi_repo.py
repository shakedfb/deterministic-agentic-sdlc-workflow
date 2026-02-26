"""Multi-repo support: parameterize MCP connections per project.

Enables the workflow to operate across different repositories
by configuring GitHub MCP connections dynamically.
"""

from __future__ import annotations

from dataclasses import dataclass

import structlog

logger = structlog.get_logger()


@dataclass
class RepoConfig:
    """Configuration for a single repository."""
    owner: str
    repo: str
    default_branch: str = "main"
    github_token: str = ""
    language: str = "python"
    test_command: str = "python -m pytest"
    e2e_test_command: str = "python -m pytest tests/e2e/"
    deploy_method: str = "terraform"


class RepoRegistry:
    """Registry of repository configurations.

    Supports multiple projects with different settings and MCP connections.
    """

    def __init__(self) -> None:
        self._repos: dict[str, RepoConfig] = {}

    def register(self, project_key: str, config: RepoConfig) -> None:
        """Register a repository configuration."""
        self._repos[project_key] = config
        logger.info("repo_registered", project=project_key, repo=f"{config.owner}/{config.repo}")

    def get(self, project_key: str) -> RepoConfig:
        """Retrieve a repository configuration by project key."""
        if project_key not in self._repos:
            raise KeyError(f"Repository not registered: {project_key}")
        return self._repos[project_key]

    def resolve_from_ticket(self, ticket_id: str) -> RepoConfig:
        """Resolve repository config from a Jira ticket ID prefix.

        Convention: ticket prefix (e.g., "PROJ" from "PROJ-123") maps to project key.
        """
        prefix = ticket_id.split("-")[0].upper()
        if prefix in self._repos:
            return self._repos[prefix]
        if "default" in self._repos:
            return self._repos["default"]
        raise KeyError(
            f"No repository configured for project prefix '{prefix}'. "
            f"Registered: {list(self._repos.keys())}"
        )

    @property
    def projects(self) -> list[str]:
        return list(self._repos.keys())


registry = RepoRegistry()


def configure_default_repos() -> None:
    """Set up default repo configurations from environment."""
    from agents.settings import settings

    if settings.github_owner and settings.github_repo:
        registry.register(
            "default",
            RepoConfig(
                owner=settings.github_owner,
                repo=settings.github_repo,
                github_token=settings.github_token,
            ),
        )

"""Unit tests for multi-repo support."""

import pytest

from agents.multi_repo import RepoConfig, RepoRegistry


class TestRepoRegistry:
    def test_register_and_get(self):
        registry = RepoRegistry()
        config = RepoConfig(owner="acme", repo="backend")
        registry.register("PROJ", config)
        assert registry.get("PROJ") == config

    def test_get_missing_raises(self):
        registry = RepoRegistry()
        with pytest.raises(KeyError):
            registry.get("MISSING")

    def test_resolve_from_ticket(self):
        registry = RepoRegistry()
        registry.register("PROJ", RepoConfig(owner="acme", repo="backend"))
        config = registry.resolve_from_ticket("PROJ-123")
        assert config.owner == "acme"

    def test_resolve_fallback_to_default(self):
        registry = RepoRegistry()
        registry.register("default", RepoConfig(owner="acme", repo="main"))
        config = registry.resolve_from_ticket("UNKNOWN-999")
        assert config.owner == "acme"

    def test_resolve_no_match_raises(self):
        registry = RepoRegistry()
        with pytest.raises(KeyError):
            registry.resolve_from_ticket("NOPE-1")

    def test_projects_list(self):
        registry = RepoRegistry()
        registry.register("A", RepoConfig(owner="a", repo="a"))
        registry.register("B", RepoConfig(owner="b", repo="b"))
        assert set(registry.projects) == {"A", "B"}

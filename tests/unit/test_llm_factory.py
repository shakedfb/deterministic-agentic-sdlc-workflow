"""Unit tests for the LLM factory (agents/llm.py)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agents.llm import get_llm, _resolve_api_key, _resolve_base_url, _resolve_model


@pytest.fixture(autouse=True)
def _clear_lru_cache():
    """Clear the LRU cache between tests so each test gets a fresh LLM instance."""
    get_llm.cache_clear()
    yield
    get_llm.cache_clear()


class TestResolveModel:
    def test_explicit_model_takes_precedence(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_model = "my-model"
            mock.llm_provider = "openai"
            mock.openai_model = "gpt-4o"
            assert _resolve_model() == "my-model"

    def test_falls_back_to_openai_model_setting(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_model = ""
            mock.llm_provider = "openai"
            mock.openai_model = "gpt-4o-mini"
            assert _resolve_model() == "gpt-4o-mini"

    def test_falls_back_to_provider_default(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_model = ""
            mock.llm_provider = "anthropic"
            mock.openai_model = ""
            assert _resolve_model() == "claude-sonnet-4-20250514"


class TestResolveApiKey:
    def test_generic_key_takes_precedence(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_api_key = "generic-key"
            mock.llm_provider = "openai"
            mock.openai_api_key = "openai-key"
            assert _resolve_api_key() == "generic-key"

    def test_falls_back_to_openai_key(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_api_key = ""
            mock.llm_provider = "openai"
            mock.openai_api_key = "openai-key"
            assert _resolve_api_key() == "openai-key"

    def test_falls_back_to_anthropic_key(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_api_key = ""
            mock.llm_provider = "anthropic"
            mock.anthropic_api_key = "anthropic-key"
            assert _resolve_api_key() == "anthropic-key"

    def test_ollama_needs_no_key(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_api_key = ""
            mock.llm_provider = "ollama"
            assert _resolve_api_key() == ""


class TestResolveBaseUrl:
    def test_explicit_url(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_base_url = "http://myserver:8000"
            mock.llm_provider = "openai"
            assert _resolve_base_url() == "http://myserver:8000"

    def test_ollama_default(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_base_url = ""
            mock.llm_provider = "ollama"
            assert _resolve_base_url() == "http://localhost:11434"


class TestGetLlm:
    def test_openai_provider(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_provider = "openai"
            mock.llm_model = "gpt-4o"
            mock.llm_api_key = "test-key"
            mock.llm_base_url = ""
            mock.llm_temperature = 0.0
            mock.openai_api_key = ""
            mock.openai_model = ""

            llm = get_llm()
            assert llm is not None
            assert type(llm).__name__ == "ChatOpenAI"

    def test_temperature_override(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_provider = "openai"
            mock.llm_model = "gpt-4o"
            mock.llm_api_key = "test-key"
            mock.llm_base_url = ""
            mock.llm_temperature = 0.0
            mock.openai_api_key = ""
            mock.openai_model = ""

            llm = get_llm(temperature=0.7)
            assert llm.temperature == 0.7

    def test_unsupported_provider_raises(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_provider = "nonexistent"
            mock.llm_model = "model"
            mock.llm_api_key = "key"
            mock.llm_base_url = ""
            mock.llm_temperature = 0.0
            mock.openai_api_key = ""
            mock.openai_model = ""
            mock.anthropic_api_key = ""

            with pytest.raises(ValueError, match="Unsupported LLM provider"):
                get_llm()

    def test_openai_compatible_requires_base_url(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_provider = "openai-compatible"
            mock.llm_model = "model"
            mock.llm_api_key = "key"
            mock.llm_base_url = ""
            mock.llm_temperature = 0.0
            mock.openai_api_key = ""
            mock.openai_model = ""

            with pytest.raises(ValueError, match="LLM_BASE_URL is required"):
                get_llm()

    def test_openai_compatible_with_base_url(self):
        with patch("agents.llm.settings") as mock:
            mock.llm_provider = "openai-compatible"
            mock.llm_model = "local-model"
            mock.llm_api_key = ""
            mock.llm_base_url = "http://localhost:1234/v1"
            mock.llm_temperature = 0.0
            mock.openai_api_key = ""
            mock.openai_model = ""

            llm = get_llm()
            assert type(llm).__name__ == "ChatOpenAI"

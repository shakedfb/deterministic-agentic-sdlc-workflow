"""LLM factory — returns a configured ChatModel based on settings.

Supports OpenAI, Anthropic, Ollama, and any OpenAI-compatible endpoint.
"""

from __future__ import annotations

import functools

from langchain_core.language_models.chat_models import BaseChatModel

from agents.settings import settings

# Default models per provider
_DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4o",
    "anthropic": "claude-sonnet-4-20250514",
    "ollama": "llama3.1",
    "openai-compatible": "gpt-4o",
}


def _resolve_model() -> str:
    """Return the model name, falling back to provider default."""
    if settings.llm_model:
        return settings.llm_model
    if settings.llm_provider == "openai" and settings.openai_model:
        return settings.openai_model
    return _DEFAULT_MODELS.get(settings.llm_provider, "gpt-4o")


def _resolve_api_key() -> str:
    """Return the API key, falling back to provider-specific env vars."""
    if settings.llm_api_key:
        return settings.llm_api_key
    if settings.llm_provider == "openai":
        return settings.openai_api_key
    if settings.llm_provider == "anthropic":
        return settings.anthropic_api_key
    return ""


def _resolve_base_url() -> str:
    """Return the base URL, defaulting for known providers."""
    if settings.llm_base_url:
        return settings.llm_base_url
    if settings.llm_provider == "ollama":
        return "http://localhost:11434"
    return ""


@functools.lru_cache(maxsize=8)
def get_llm(temperature: float | None = None) -> BaseChatModel:
    """Return a ChatModel instance configured from settings.

    Args:
        temperature: Override the default temperature. Uses settings.llm_temperature
                     when None.

    Returns:
        A BaseChatModel ready for use with .invoke() / .ainvoke().

    Raises:
        ValueError: If the provider is not supported or missing required config.
    """
    provider = settings.llm_provider.lower()
    model = _resolve_model()
    api_key = _resolve_api_key()
    base_url = _resolve_base_url()
    temp = temperature if temperature is not None else settings.llm_temperature

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        kwargs: dict = {"model": model, "temperature": temp}
        if api_key:
            kwargs["api_key"] = api_key
        if base_url:
            kwargs["base_url"] = base_url
        return ChatOpenAI(**kwargs)

    if provider == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError as exc:
            raise ImportError(
                "langchain-anthropic is required for the anthropic provider. "
                "Install it with: pip install 'agentic-sdlc[anthropic]'"
            ) from exc

        kwargs = {"model": model, "temperature": temp}
        if api_key:
            kwargs["api_key"] = api_key
        return ChatAnthropic(**kwargs)

    if provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError as exc:
            raise ImportError(
                "langchain-ollama is required for the ollama provider. "
                "Install it with: pip install 'agentic-sdlc[ollama]'"
            ) from exc

        return ChatOllama(
            model=model,
            temperature=temp,
            base_url=base_url or "http://localhost:11434",
        )

    if provider == "openai-compatible":
        from langchain_openai import ChatOpenAI

        if not base_url:
            raise ValueError(
                "LLM_BASE_URL is required for openai-compatible provider"
            )
        kwargs = {"model": model, "temperature": temp, "base_url": base_url}
        if api_key:
            kwargs["api_key"] = api_key
        else:
            kwargs["api_key"] = "not-needed"
        return ChatOpenAI(**kwargs)

    raise ValueError(
        f"Unsupported LLM provider: {provider!r}. "
        "Supported: openai, anthropic, ollama, openai-compatible"
    )

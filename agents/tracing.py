"""LangSmith tracing and observability utilities.

Gracefully degrades when LangSmith API key is not configured.
"""

from __future__ import annotations

import functools
from typing import Any, Callable

import structlog

from agents.settings import settings

logger = structlog.get_logger()

_client: Any = None


def get_langsmith_client():
    """Return a LangSmith Client, or None if the API key is not configured."""
    global _client
    if _client is None:
        if not settings.langsmith_api_key:
            return None
        try:
            from langsmith import Client

            _client = Client(api_key=settings.langsmith_api_key)
        except Exception:
            return None
    return _client


def trace_phase(phase: str, **run_metadata: Any) -> Callable:
    """Decorator that wraps a function in a LangSmith trace with phase metadata.

    When LangSmith is not configured, the decorator is a simple pass-through
    that still logs start/end via structlog.
    """

    def decorator(fn: Callable) -> Callable:
        # Only apply @traceable when LangSmith is configured
        inner = fn
        if settings.langsmith_api_key:
            try:
                from langsmith import traceable

                inner = traceable(
                    name=f"sdlc.{phase}.{fn.__name__}",
                    project_name=settings.langsmith_project,
                    metadata={"phase": phase, **run_metadata},
                )(fn)
            except Exception:
                pass

        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            await logger.ainfo(
                "trace_start",
                phase=phase,
                function=fn.__name__,
                metadata=run_metadata,
            )
            try:
                result = await inner(*args, **kwargs)
                await logger.ainfo("trace_end", phase=phase, function=fn.__name__, success=True)
                return result
            except Exception as exc:
                await logger.aerror(
                    "trace_end",
                    phase=phase,
                    function=fn.__name__,
                    success=False,
                    error=str(exc),
                )
                raise

        return wrapper

    return decorator


def log_feedback(run_id: str, key: str, score: float, comment: str = "") -> None:
    """Log evaluation feedback to LangSmith for a given run."""
    client = get_langsmith_client()
    if client is None:
        return
    client.create_feedback(
        run_id=run_id,
        key=key,
        score=score,
        comment=comment,
    )

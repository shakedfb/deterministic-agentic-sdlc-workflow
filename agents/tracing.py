"""LangSmith tracing and observability utilities."""

from __future__ import annotations

import functools
from typing import Any, Callable

import structlog
from langsmith import Client, traceable

from agents.settings import settings

logger = structlog.get_logger()

_client: Client | None = None


def get_langsmith_client() -> Client:
    global _client
    if _client is None:
        _client = Client(
            api_key=settings.langsmith_api_key,
        )
    return _client


def trace_phase(phase: str, **run_metadata: Any) -> Callable:
    """Decorator that wraps a function in a LangSmith trace with phase metadata."""

    def decorator(fn: Callable) -> Callable:
        @traceable(
            name=f"sdlc.{phase}.{fn.__name__}",
            project_name=settings.langsmith_project,
            metadata={"phase": phase, **run_metadata},
        )
        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            await logger.ainfo(
                "trace_start",
                phase=phase,
                function=fn.__name__,
                metadata=run_metadata,
            )
            try:
                result = await fn(*args, **kwargs)
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
    client.create_feedback(
        run_id=run_id,
        key=key,
        score=score,
        comment=comment,
    )

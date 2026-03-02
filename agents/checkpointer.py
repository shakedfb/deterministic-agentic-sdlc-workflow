"""LangGraph checkpoint store with PostgreSQL primary and in-memory fallback."""

from __future__ import annotations

import structlog

from agents.settings import settings

logger = structlog.get_logger()


async def create_checkpointer():
    """Create a checkpointer, falling back to MemorySaver when PostgreSQL is unavailable."""
    if settings.postgres_url:
        try:
            from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

            checkpointer = AsyncPostgresSaver.from_conn_string(settings.postgres_url)
            await checkpointer.setup()
            return checkpointer
        except Exception as exc:
            await logger.awarn(
                "postgres_checkpointer_unavailable",
                error=str(exc),
                fallback="MemorySaver",
            )

    from langgraph.checkpoint.memory import MemorySaver

    await logger.ainfo("using_memory_checkpointer")
    return MemorySaver()

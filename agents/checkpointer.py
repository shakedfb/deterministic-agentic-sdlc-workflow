"""LangGraph checkpoint store backed by PostgreSQL for durable state."""

from __future__ import annotations

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agents.settings import settings


async def create_checkpointer() -> AsyncPostgresSaver:
    """Create and initialize a PostgreSQL-backed async checkpointer."""
    checkpointer = AsyncPostgresSaver.from_conn_string(settings.postgres_url)
    await checkpointer.setup()
    return checkpointer

"""Memory subsystem: Redis for short-term state, Pinecone for long-term retrieval.

Both degrade to in-memory alternatives when external services are unavailable.
"""

from __future__ import annotations

import json
from typing import Any

import structlog

from agents.models import WorkflowState
from agents.settings import settings

logger = structlog.get_logger()


class RedisStateStore:
    """Short-term state store using Redis. Falls back to an in-memory dict."""

    def __init__(self, url: str | None = None):
        self._url = url or settings.redis_url
        self._client: Any = None
        self._fallback: dict[str, str] = {}
        self._use_fallback: bool = False

    async def _get_client(self):
        if self._use_fallback:
            return None
        if self._client is None:
            try:
                import redis.asyncio as aioredis

                self._client = aioredis.from_url(self._url, decode_responses=True)
                await self._client.ping()
            except Exception as exc:
                await logger.awarn("redis_unavailable", error=str(exc), fallback="in-memory dict")
                self._use_fallback = True
                self._client = None
                return None
        return self._client

    def _key(self, ticket_id: str, suffix: str = "state") -> str:
        return f"sdlc:{ticket_id}:{suffix}"

    async def save_state(self, state: WorkflowState, ttl: int = 86400) -> None:
        key = self._key(state.ticket_id)
        client = await self._get_client()
        if client is None:
            self._fallback[key] = state.model_dump_json()
        else:
            await client.set(key, state.model_dump_json(), ex=ttl)
        await logger.ainfo("state_saved", ticket_id=state.ticket_id, phase=state.phase.value)

    async def load_state(self, ticket_id: str) -> WorkflowState | None:
        key = self._key(ticket_id)
        client = await self._get_client()
        if client is None:
            data = self._fallback.get(key)
        else:
            data = await client.get(key)
        if data is None:
            return None
        return WorkflowState.model_validate_json(data)

    async def save_artifact(self, ticket_id: str, artifact_type: str, data: dict) -> None:
        key = self._key(ticket_id, artifact_type)
        client = await self._get_client()
        if client is None:
            self._fallback[key] = json.dumps(data)
        else:
            await client.set(key, json.dumps(data), ex=86400)

    async def load_artifact(self, ticket_id: str, artifact_type: str) -> dict | None:
        key = self._key(ticket_id, artifact_type)
        client = await self._get_client()
        if client is None:
            data = self._fallback.get(key)
        else:
            data = await client.get(key)
        return json.loads(data) if data else None

    async def close(self) -> None:
        if self._client:
            await self._client.close()


class VectorMemory:
    """Long-term memory store using Pinecone. Falls back to in-memory list."""

    def __init__(
        self,
        api_key: str | None = None,
        index_name: str | None = None,
        embeddings: Any | None = None,
    ):
        self._api_key = api_key or settings.pinecone_api_key
        self._index_name = index_name or settings.pinecone_index
        self._embeddings = embeddings
        self._pc: Any = None
        self._index: Any = None
        self._use_fallback: bool = not self._api_key
        self._fallback_store: list[dict[str, Any]] = []

    def _ensure_embeddings(self):
        if self._embeddings is None:
            from langchain_openai import OpenAIEmbeddings
            self._embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        return self._embeddings

    def _get_index(self):
        if self._use_fallback:
            return None
        if self._index is None:
            try:
                from pinecone import Pinecone
                self._pc = Pinecone(api_key=self._api_key)
                self._index = self._pc.Index(self._index_name)
            except Exception:
                self._use_fallback = True
                return None
        return self._index

    async def store(
        self, text: str, metadata: dict[str, Any], namespace: str = "default"
    ) -> str:
        """Embed and store a text with metadata. Returns the vector ID."""
        vec_id = f"{namespace}:{metadata.get('ticket_id', 'unknown')}:{hash(text) & 0xFFFFFFFF:08x}"

        if self._use_fallback or self._get_index() is None:
            self._fallback_store.append({"id": vec_id, "text": text, "metadata": metadata, "namespace": namespace})
            await logger.ainfo("vector_stored_inmemory", vec_id=vec_id, namespace=namespace)
            return vec_id

        embeddings = self._ensure_embeddings()
        embedding = await embeddings.aembed_query(text)
        index = self._get_index()
        index.upsert(
            vectors=[{"id": vec_id, "values": embedding, "metadata": {**metadata, "text": text}}],
            namespace=namespace,
        )
        await logger.ainfo("vector_stored", vec_id=vec_id, namespace=namespace)
        return vec_id

    async def search(
        self, query: str, namespace: str = "default", top_k: int = 5
    ) -> list[dict[str, Any]]:
        """Semantic search over stored vectors. Returns metadata with scores."""
        if self._use_fallback or self._get_index() is None:
            await logger.ainfo("vector_search_inmemory", namespace=namespace)
            return []

        embeddings = self._ensure_embeddings()
        embedding = await embeddings.aembed_query(query)
        index = self._get_index()
        results = index.query(
            vector=embedding, top_k=top_k, include_metadata=True, namespace=namespace
        )
        return [
            {"score": match.score, **match.metadata}
            for match in results.matches
        ]

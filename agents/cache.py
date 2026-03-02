"""Content-addressable cache for skipping redundant LLM generations.

Uses Redis with SHA-256 hashing of inputs to detect identical subtasks.
Falls back to an in-memory dict when Redis is unavailable.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

import structlog

from agents.settings import settings

logger = structlog.get_logger()

CACHE_PREFIX = "cache:gen:"
CACHE_TTL = 86400 * 7  # 7 days


class GenerationCache:
    """Content-addressable cache backed by Redis.

    Caches LLM generation results keyed by a hash of the input (prompt + context).
    Prevents redundant LLM calls for identical subtasks across tickets.
    Falls back to an in-memory dict when Redis is unavailable.
    """

    def __init__(self, url: str | None = None):
        self._url = url or settings.redis_url
        self._client: Any = None
        self._hits = 0
        self._misses = 0
        self._use_fallback: bool = False
        self._fallback: dict[str, str] = {}

    async def _get_client(self):
        if self._use_fallback:
            return None
        if self._client is None:
            try:
                import redis.asyncio as aioredis

                self._client = aioredis.from_url(self._url, decode_responses=True)
                await self._client.ping()
            except Exception as exc:
                await logger.awarn("redis_cache_unavailable", error=str(exc), fallback="in-memory dict")
                self._use_fallback = True
                self._client = None
                return None
        return self._client

    @staticmethod
    def _hash_key(inputs: dict[str, Any]) -> str:
        """Compute a deterministic SHA-256 hash of the input dict."""
        canonical = json.dumps(inputs, sort_keys=True, default=str)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def _key(self, hash_val: str) -> str:
        return f"{CACHE_PREFIX}{hash_val}"

    async def get(self, inputs: dict[str, Any]) -> dict[str, Any] | None:
        """Look up a cached result by input hash. Returns None on miss."""
        h = self._hash_key(inputs)
        client = await self._get_client()

        if client is None:
            cached = self._fallback.get(self._key(h))
        else:
            cached = await client.get(self._key(h))

        if cached is not None:
            self._hits += 1
            await logger.ainfo("cache_hit", hash=h[:12], total_hits=self._hits)
            return json.loads(cached)

        self._misses += 1
        return None

    async def put(self, inputs: dict[str, Any], result: dict[str, Any]) -> str:
        """Store a generation result. Returns the cache key hash."""
        h = self._hash_key(inputs)
        value = json.dumps(result, default=str)
        client = await self._get_client()

        if client is None:
            self._fallback[self._key(h)] = value
        else:
            await client.set(self._key(h), value, ex=CACHE_TTL)

        await logger.ainfo("cache_store", hash=h[:12])
        return h

    async def invalidate(self, inputs: dict[str, Any]) -> bool:
        """Invalidate a cached entry. Returns True if it existed."""
        h = self._hash_key(inputs)
        client = await self._get_client()

        if client is None:
            return self._fallback.pop(self._key(h), None) is not None

        deleted = await client.delete(self._key(h))
        return deleted > 0

    @property
    def stats(self) -> dict[str, int]:
        total = self._hits + self._misses
        return {
            "hits": self._hits,
            "misses": self._misses,
            "total": total,
            "hit_rate": round(self._hits / total, 3) if total > 0 else 0,
        }

    async def close(self) -> None:
        if self._client:
            await self._client.close()

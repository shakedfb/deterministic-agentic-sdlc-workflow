"""Unit tests for the content-addressable generation cache."""

import pytest

from agents.cache import GenerationCache


class TestGenerationCache:
    def test_hash_determinism(self):
        inputs = {"subtask": "implement auth", "context": "flask app"}
        h1 = GenerationCache._hash_key(inputs)
        h2 = GenerationCache._hash_key(inputs)
        assert h1 == h2

    def test_hash_differs_on_change(self):
        h1 = GenerationCache._hash_key({"a": 1})
        h2 = GenerationCache._hash_key({"a": 2})
        assert h1 != h2

    def test_hash_key_order_independence(self):
        h1 = GenerationCache._hash_key({"a": 1, "b": 2})
        h2 = GenerationCache._hash_key({"b": 2, "a": 1})
        assert h1 == h2

    def test_stats_initial(self):
        cache = GenerationCache()
        assert cache.stats == {"hits": 0, "misses": 0, "total": 0, "hit_rate": 0}

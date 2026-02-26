"""Unit tests for parallel task execution logic."""

import pytest

from agents.parallel import _classify_dependencies


class TestDependencyClassification:
    def test_independent_tasks(self):
        subtasks = [
            {"name": "a", "files_to_create": ["a.py"], "files_to_modify": []},
            {"name": "b", "files_to_create": ["b.py"], "files_to_modify": []},
            {"name": "c", "files_to_create": ["c.py"], "files_to_modify": []},
        ]
        layers, order = _classify_dependencies(subtasks)
        assert len(layers) == 1
        assert set(layers[0]) == {0, 1, 2}

    def test_linear_chain(self):
        subtasks = [
            {"name": "a", "files_to_create": ["a.py"], "files_to_modify": []},
            {"name": "b", "files_to_create": ["b.py"], "files_to_modify": ["a.py"]},
            {"name": "c", "files_to_create": ["c.py"], "files_to_modify": ["b.py"]},
        ]
        layers, order = _classify_dependencies(subtasks)
        assert len(layers) == 3
        assert layers[0] == [0]
        assert layers[1] == [1]
        assert layers[2] == [2]

    def test_diamond_dependency(self):
        subtasks = [
            {"name": "base", "files_to_create": ["base.py"], "files_to_modify": []},
            {"name": "left", "files_to_create": ["left.py"], "files_to_modify": ["base.py"]},
            {"name": "right", "files_to_create": ["right.py"], "files_to_modify": ["base.py"]},
            {"name": "top", "files_to_create": ["top.py"], "files_to_modify": ["left.py", "right.py"]},
        ]
        layers, order = _classify_dependencies(subtasks)
        assert layers[0] == [0]
        assert set(layers[1]) == {1, 2}
        assert layers[2] == [3]

    def test_empty_subtasks(self):
        layers, order = _classify_dependencies([])
        assert layers == []
        assert order == []

"""Unit tests for LangGraph subgraph structure (no LLM calls)."""

import pytest
from langgraph.graph import StateGraph

from agents.intake.graph import build_intake_graph
from agents.development.graph import build_dev_graph
from agents.e2e_testing.graph import build_e2e_graph
from agents.review.graph import build_review_graph
from agents.deployment.graph import build_deploy_graph


class TestIntakeGraph:
    def test_builds_without_error(self):
        graph = build_intake_graph()
        assert isinstance(graph, StateGraph)

    def test_compiles_without_checkpointer(self):
        from agents.intake.graph import compile_intake_graph
        compiled = compile_intake_graph()
        assert compiled is not None

    def test_has_expected_nodes(self):
        graph = build_intake_graph()
        node_names = set(graph.nodes.keys())
        assert "parse_ticket" in node_names
        assert "enrich_context" in node_names
        assert "generate_spec" in node_names


class TestDevGraph:
    def test_builds_without_error(self):
        graph = build_dev_graph()
        assert isinstance(graph, StateGraph)

    def test_compiles_without_checkpointer(self):
        from agents.development.graph import compile_dev_graph
        compiled = compile_dev_graph()
        assert compiled is not None

    def test_has_expected_nodes(self):
        graph = build_dev_graph()
        node_names = set(graph.nodes.keys())
        expected = {"plan_tasks", "generate_code", "generate_tests", "execute_tests", "analyze_results"}
        assert expected.issubset(node_names)


class TestE2EGraph:
    def test_builds_without_error(self):
        graph = build_e2e_graph()
        assert isinstance(graph, StateGraph)

    def test_compiles(self):
        from agents.e2e_testing.graph import compile_e2e_graph
        compiled = compile_e2e_graph()
        assert compiled is not None

    def test_has_expected_nodes(self):
        graph = build_e2e_graph()
        node_names = set(graph.nodes.keys())
        expected = {"provision_environment", "generate_e2e_tests", "execute_e2e", "analyze_e2e"}
        assert expected.issubset(node_names)


class TestReviewGraph:
    def test_builds_without_error(self):
        graph = build_review_graph()
        assert isinstance(graph, StateGraph)

    def test_compiles(self):
        from agents.review.graph import compile_review_graph
        compiled = compile_review_graph()
        assert compiled is not None

    def test_has_expected_nodes(self):
        graph = build_review_graph()
        node_names = set(graph.nodes.keys())
        expected = {"security_review", "scale_review", "reliability_review"}
        assert expected.issubset(node_names)


class TestDeployGraph:
    def test_builds_without_error(self):
        graph = build_deploy_graph()
        assert isinstance(graph, StateGraph)

    def test_compiles(self):
        from agents.deployment.graph import compile_deploy_graph
        compiled = compile_deploy_graph()
        assert compiled is not None

    def test_has_expected_nodes(self):
        graph = build_deploy_graph()
        node_names = set(graph.nodes.keys())
        expected = {"generate_terraform", "terraform_plan", "terraform_apply", "health_check", "rollback"}
        assert expected.issubset(node_names)

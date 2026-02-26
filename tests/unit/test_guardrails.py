"""Unit tests for guardrail validators."""

import pytest

from config.guardrails_code import (
    CodeValidationResult,
    scan_for_anti_patterns,
    scan_for_secrets,
    validate_code,
    validate_python_syntax,
)
from config.guardrails_spec import SpecValidationResult, validate_requirement_spec
from config.guardrails_terraform import TerraformValidationResult, validate_terraform_plan


class TestSpecValidation:
    def test_valid_spec(self):
        spec = {
            "title": "Add user authentication",
            "feature_description": "Implement JWT-based authentication with login and signup",
            "acceptance_criteria": [
                {"description": "Users can log in", "testable": True},
            ],
            "affected_components": ["auth/"],
        }
        result = validate_requirement_spec(spec)
        assert result.valid is True
        assert result.errors == []

    def test_missing_title(self):
        spec = {
            "title": "",
            "feature_description": "A long enough description here",
            "acceptance_criteria": [{"description": "test", "testable": True}],
            "affected_components": ["src/"],
        }
        result = validate_requirement_spec(spec)
        assert result.valid is False
        assert any("Title" in e for e in result.errors)

    def test_missing_criteria(self):
        spec = {
            "title": "Valid Title",
            "feature_description": "A long enough description here",
            "acceptance_criteria": [],
            "affected_components": ["src/"],
        }
        result = validate_requirement_spec(spec)
        assert result.valid is False
        assert any("acceptance criterion" in e for e in result.errors)

    def test_missing_components(self):
        spec = {
            "title": "Valid Title",
            "feature_description": "A long enough description here",
            "acceptance_criteria": [{"description": "test", "testable": True}],
            "affected_components": [],
        }
        result = validate_requirement_spec(spec)
        assert result.valid is False
        assert any("component" in e for e in result.errors)


class TestCodeValidation:
    def test_valid_python(self):
        code = "def hello():\n    return 'world'\n"
        result = validate_code(code, "python")
        assert result.valid is True

    def test_syntax_error(self):
        code = "def hello(\n    return 'world'\n"
        result = validate_code(code, "python")
        assert result.valid is False
        assert any("Syntax error" in e for e in result.errors)

    def test_secret_detection(self):
        code = 'API_KEY = "sk-abc123456789012345678901234567890"\n'
        result = validate_code(code, "python")
        assert result.valid is False
        assert any("secret" in e.lower() or "Secret" in e for e in result.errors)

    def test_anti_patterns(self):
        code = "result = eval(user_input)\n"
        result = validate_code(code, "python")
        assert len(result.warnings) > 0
        assert any("eval" in w for w in result.warnings)

    def test_aws_key_detection(self):
        code = 'key = "AKIAIOSFODNN7EXAMPLE"\n'
        secrets = scan_for_secrets(code)
        assert len(secrets) > 0


class TestTerraformValidation:
    def test_safe_plan(self):
        plan = """
        # aws_instance.web will be created
        + resource "aws_instance" "web" {
            ami           = "ami-12345"
            instance_type = "t3.micro"
          }

        Plan: 1 to add, 0 to change, 0 to destroy.
        """
        result = validate_terraform_plan(plan)
        assert result.safe is True
        assert result.resources_created == 1

    def test_dangerous_db_destroy(self):
        plan = """
        # aws_rds_cluster.production will be destroyed
        - resource "aws_rds_cluster" "production" {
          }

        Plan: 0 to add, 0 to change, 1 to destroy.
        """
        result = validate_terraform_plan(plan)
        assert result.safe is False
        assert len(result.errors) > 0

    def test_public_exposure(self):
        plan = """
        cidr_blocks = ["0.0.0.0/0"]
        """
        result = validate_terraform_plan(plan)
        assert result.safe is False

    def test_large_destroy_warning(self):
        lines = "\n".join(
            f"# aws_instance.worker_{i} will be destroyed" for i in range(10)
        )
        plan = f"{lines}\nPlan: 0 to add, 0 to change, 10 to destroy."
        result = validate_terraform_plan(plan)
        assert any("Large number" in w for w in result.warnings)

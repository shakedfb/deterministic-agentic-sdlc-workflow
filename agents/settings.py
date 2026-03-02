"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    # LLM provider
    llm_provider: str = "openai"  # openai | anthropic | ollama | openai-compatible
    llm_model: str = ""  # empty = provider default
    llm_base_url: str = ""  # required for ollama and openai-compatible
    llm_api_key: str = ""  # generic key, falls back to provider-specific env vars
    llm_temperature: float = 0.0

    # Provider-specific keys (used as fallbacks when llm_api_key is empty)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    anthropic_api_key: str = ""

    # LangSmith
    langsmith_api_key: str = ""
    langsmith_project: str = "agentic-sdlc"
    langchain_tracing_v2: bool = True

    # Temporal
    temporal_host: str = "localhost:7233"
    temporal_namespace: str = "agentic-sdlc"
    temporal_task_queue: str = "sdlc-workflow"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # PostgreSQL
    postgres_url: str = "postgresql://agentic:agentic@localhost:5432/agentic_sdlc"

    # E2B
    e2b_api_key: str = ""

    # Pinecone
    pinecone_api_key: str = ""
    pinecone_index: str = "agentic-sdlc-memory"

    # Jira
    jira_base_url: str = ""
    jira_api_token: str = ""
    jira_user_email: str = ""

    # GitHub
    github_token: str = ""
    github_owner: str = ""
    github_repo: str = ""

    # Slack
    slack_bot_token: str = ""
    slack_hitl_channel: str = ""

    # Terraform
    tf_state_bucket: str = ""
    tf_state_region: str = "us-east-1"

    # Retry budgets
    max_unit_test_retries: int = 3
    max_e2e_retries: int = 2
    max_intake_retries: int = 1

    # Timeouts (seconds)
    intake_timeout: int = 300
    dev_timeout: int = 1800
    e2e_timeout: int = 1200
    review_timeout: int = 600
    deploy_timeout: int = 900

    # HITL
    hitl_timeout_hours: int = 4
    hitl_escalation_hours: int = 8

    # Guardrails
    min_coverage_percent: float = Field(default=80.0, ge=0, le=100)


settings = Settings()

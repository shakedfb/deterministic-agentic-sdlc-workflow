# Agentic SDLC Workflow

A deterministic agentic workflow that automates the software development lifecycle — from Jira ticket intake through code generation, testing, review, and IaC deployment.

## Architecture

**Two-layer design:**

- **Layer 1 — Temporal** provides durable orchestration: retries, timeouts, crash recovery, exactly-once semantics.
- **Layer 2 — LangGraph** provides agent logic: cyclic subgraphs with conditional branching, state-driven LLM reasoning.

**Four subsystems:**

| Subsystem | Technology | Role |
|-----------|------------|------|
| Brain | LangGraph + Temporal | Orchestration and decision-making |
| Memory | Redis + Pinecone + LangGraph checkpoints | Short-term state, long-term retrieval, workflow resumption |
| Hands | MCP servers + E2B sandboxes | External system access and code execution |
| Eyes | LangSmith + Guardrails AI | Observability, tracing, output validation |

## Pipeline Stages

1. **Intake** — Parse Jira tickets, enrich with codebase context, generate structured specs
2. **Development** — Generate code + unit tests, execute in sandbox, retry on failure
3. **E2E Testing** — Provision isolated environment, run end-to-end tests
4. **Review** — Security, scale, and reliability analysis
5. **Deployment** — Generate Terraform, plan, human approval, apply, health check

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Copy and configure environment
cp .env.example .env

# Start infrastructure
docker compose up -d

# Run the Temporal worker
python -m orchestrator.worker

# Trigger a workflow (from a Jira ticket)
python -m orchestrator.trigger --ticket-id PROJ-123
```

## Project Structure

```
orchestrator/       # Temporal workflows and workers
agents/             # LangGraph subgraphs per pipeline stage
  intake/           # Requirement parsing and spec generation
  development/      # Code generation and unit testing
  e2e_testing/      # End-to-end test generation and execution
  review/           # Security, scale, reliability review
  deployment/       # Terraform generation and deployment
mcp_servers/        # MCP server implementations
  jira/             # Jira ticket read/write
  github/           # GitHub repository operations
  terraform/        # Terraform plan/apply
  docker/           # Docker Compose lifecycle
  slack/            # HITL notifications
  semgrep/          # Static analysis
config/             # Guardrails rail configs and prompt templates
infra/              # Terraform for the platform itself
tests/              # Unit, integration, and E2E tests
```

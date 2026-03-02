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

### Prerequisites

- **Docker** (for Temporal + supporting services)
- **Python 3.11+**
- **An LLM** — one of: [Ollama](https://ollama.com) (free, local), OpenAI API key, or Anthropic API key

### 1. Install

```bash
pip install -e ".[all-providers,dev]"
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` and set your LLM provider. Everything else is optional — Redis, PostgreSQL, Pinecone, Jira, and Slack all degrade gracefully to local fallbacks when unconfigured.

**Ollama (zero API keys):**
```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1
```
```bash
ollama pull llama3.1  # one-time download
```

**OpenAI:**
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
```

**Anthropic:**
```env
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-...
```

### 3. Start infrastructure

```bash
docker compose up -d
```

This starts Temporal (`:7233`), Temporal UI (`:8080`), PostgreSQL (`:5432`), and Redis (`:6379`). Wait ~15 seconds for Temporal to bootstrap.

### 4. Start the worker

```bash
python -m orchestrator.worker
```

### 5. Trigger a workflow

In a separate terminal:

```bash
# Plain-text description (no Jira needed)
python -m orchestrator.local_trigger "Build a REST API that returns user profiles by ID"

# From a file
python -m orchestrator.local_trigger --file spec.txt

# Interactive (type/paste, Ctrl+D to submit)
python -m orchestrator.local_trigger --interactive

# With title and priority
python -m orchestrator.local_trigger "Add OAuth2 login" --title "OAuth2 Feature" --priority High

# From a Jira ticket (requires JIRA_* config)
python -m orchestrator.trigger --ticket-id PROJ-123
```

### 6. Monitor

Open **http://localhost:8080** to watch the workflow progress through Intake → Development → E2E Testing → Review → Deployment.

### Teardown

```bash
docker compose down        # stop services, keep data
docker compose down -v     # stop services, delete volumes
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

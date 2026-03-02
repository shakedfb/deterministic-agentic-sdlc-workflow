# Operational Runbook

## Local Development Setup

### LLM Provider Configuration

The system supports four LLM providers. Set `LLM_PROVIDER` in `.env`:

| Provider | `LLM_PROVIDER` | API Key Required | Extra Install |
|----------|----------------|-----------------|---------------|
| OpenAI | `openai` | Yes (`LLM_API_KEY` or `OPENAI_API_KEY`) | — (included) |
| Anthropic | `anthropic` | Yes (`LLM_API_KEY` or `ANTHROPIC_API_KEY`) | `pip install -e ".[anthropic]"` |
| Ollama | `ollama` | No | `pip install -e ".[ollama]"` + `ollama pull <model>` |
| OpenAI-compatible (LM Studio, vLLM, etc.) | `openai-compatible` | Varies | `LLM_BASE_URL` required |

Use `pip install -e ".[all-providers,dev]"` to install everything.

### Service Fallback Behavior

Only Temporal is required to run workflows. Everything else degrades gracefully:

| Service | Required? | Fallback When Absent |
|---------|-----------|---------------------|
| Temporal | **Yes** | No fallback — workflow orchestration needs it |
| PostgreSQL | No | LangGraph checkpoints use in-memory `MemorySaver` |
| Redis | No | State store and generation cache use in-memory `dict` |
| Pinecone | No | Vector search returns empty results; stores in-memory list |
| E2B | No | Test execution simulated (all tests "pass") |
| LangSmith | No | Tracing disabled; structlog still logs locally |
| Jira | No | Use `local_trigger.py` with synthetic `LOCAL-XXXXXX` ticket IDs |
| Slack | No | HITL notifications print to console |
| Semgrep | No | SAST step skipped in review |
| Terraform CLI | No | Plan/apply simulated |

### Minimal Run (Ollama, No External Services)

```bash
# .env — only two lines needed
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1

# Start just Temporal (Redis/Postgres optional but included)
docker compose up -d

# Worker (terminal 1)
python -m orchestrator.worker

# Trigger (terminal 2)
python -m orchestrator.local_trigger "Build a REST API that returns user profiles by ID"

# Monitor at http://localhost:8080
```

### HITL Approval in Local Mode

Without Slack, HITL requests print to the console. Send approval signals via Temporal CLI:

```bash
# Approve a deployment
temporal workflow signal \
  --workflow-id sdlc-LOCAL-ABC123 \
  --name hitl_response \
  --input '{"action":"approve","actor":"local-dev"}'

# Reject
temporal workflow signal \
  --workflow-id sdlc-LOCAL-ABC123 \
  --name hitl_response \
  --input '{"action":"reject","actor":"local-dev"}'
```

### Running Tests

```bash
pytest tests/unit/ -v          # Unit tests (no infra needed)
pytest tests/ -v               # All tests
```

## Stuck Workflows

### Symptoms
- Workflow in Temporal UI shows "Running" for >2x expected duration
- No heartbeats from activity in the last 5 minutes

### Resolution
1. Check Temporal UI at `http://localhost:8080` for workflow details
2. Inspect the activity task queue for pending tasks
3. If the worker is down:
   ```bash
   # Check worker process
   docker compose ps
   # Restart worker
   python -m orchestrator.worker
   ```
4. If stuck on HITL:
   ```bash
   # Send approval signal via Temporal CLI
   temporal workflow signal --workflow-id sdlc-PROJ-123 --name hitl_response --input '{"action":"approve","actor":"ops-team"}'
   ```
5. If the LangGraph subgraph is stuck mid-node:
   - Check the checkpoint store for the thread
   - The next Temporal retry will resume from the last checkpoint

## HITL Queue Backlog

### Symptoms
- Multiple workflows waiting for human approval
- Slack channel has unanswered HITL requests

### Resolution
1. Check the admin dashboard: `GET /metrics`
2. Process HITL queue in priority order (deployment > review > development > e2e > intake)
3. For deployment approvals, review the Terraform plan before sending signal
4. If timeout is approaching (8h), either approve/reject or the workflow auto-cancels

## Temporal Cluster Maintenance

### Health Check
```bash
temporal operator cluster health
```

### Rolling Restart
```bash
# Workers are stateless; restart one at a time
docker compose restart temporal
# Wait for temporal to be healthy
docker compose exec temporal temporal operator cluster health
```

### Database Maintenance
```bash
# PostgreSQL vacuum
docker compose exec postgres psql -U temporal -c "VACUUM ANALYZE;"
```

## Secret Rotation

### API Keys
1. Generate new key in the provider's dashboard
2. Update `.env` file with the new key
3. Restart the worker process
4. Verify with a test workflow trigger

### GitHub Token
1. Create new fine-grained token with `repo` and `pull_request` scopes
2. Update `GITHUB_TOKEN` in `.env`
3. Restart worker

### Process
- Rotate all credentials quarterly
- Use the security audit to verify: `python -c "from agents.security import run_full_audit; print(run_full_audit())"`

## Scaling Workers

### Horizontal Scaling
```bash
# Run multiple worker instances (each picks up tasks from the same queue)
python -m orchestrator.worker &
python -m orchestrator.worker &
python -m orchestrator.worker &
```

### Monitoring Worker Load
- Check Temporal UI for task queue depth
- If queue depth > 10 consistently, add more workers
- Each worker handles one activity at a time by default

## Common Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `LLM API timeout` | Provider rate limit or outage | Temporal auto-retries; check provider status |
| `Sandbox OOM` | Generated code consumes too much memory | Increase E2B sandbox memory or simplify the task |
| `Terraform plan unsafe` | Generated TF has dangerous operations | Review guardrail errors; may need HITL |
| `HITL timeout` | No human responded within 8 hours | Workflow auto-cancels; check Slack channel |
| `Checkpoint load failed` | PostgreSQL connectivity issue | Check DB health; workflow will retry |

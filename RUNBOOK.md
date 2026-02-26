# Operational Runbook

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

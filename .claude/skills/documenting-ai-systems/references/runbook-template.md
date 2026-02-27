# Runbook Template

```markdown
# Runbook: [System Name]

## Overview
- **Service**: [name and purpose]
- **Owner**: [team/person]
- **Tier**: [P1/P2/P3]
- **Architecture**: [link to architecture doc]

## Quick Reference
| Item | Value |
|------|-------|
| API URL | https://api.example.com |
| Health endpoint | /health |
| Logs | [log location/service] |
| Traces | [Langfuse/LangSmith URL] |
| Alerts | [PagerDuty/Slack channel] |

## Common Operations

### Restart Service
```bash
docker-compose restart agent-api
# or
kubectl rollout restart deployment/agent-api
```

### Check Health
```bash
curl https://api.example.com/health
```

### View Logs
```bash
docker-compose logs -f agent-api --tail=100
# or
kubectl logs -f deployment/agent-api
```

### Scale Up
```bash
kubectl scale deployment/agent-api --replicas=4
```

## Incident Response

### High Error Rate (>5%)
1. Check logs for error patterns
2. Check LLM provider status pages
3. If provider down: verify fallback chain is active
4. If our code: roll back to last known good deploy

### High Latency (P95 >10s)
1. Check `nvidia-smi` if GPU serving
2. Check vector DB query times
3. Check LLM provider latency
4. Scale up if traffic spike

### Cost Spike
1. Check per-model cost in Langfuse
2. Identify which agent/prompt is expensive
3. Check for infinite loops (max_iterations hit?)
4. Add/tighten rate limits

### Vector DB Down
1. Check Qdrant health: `curl http://localhost:6333/healthz`
2. Check disk space: `df -h`
3. Restart: `docker-compose restart qdrant`
4. If data corrupt: restore from backup

## Deployment
1. Run eval gate: `npx promptfoo eval --ci`
2. Build image: `docker build -t agent-api:$SHA .`
3. Deploy: `kubectl set image deployment/agent-api agent-api=agent-api:$SHA`
4. Monitor: watch health endpoint and error rate for 15 min
5. Rollback if issues: `kubectl rollout undo deployment/agent-api`
```

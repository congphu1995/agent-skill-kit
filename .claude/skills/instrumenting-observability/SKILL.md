---
name: instrumenting-observability
description: >
  Add observability to AI systems: tracing (Langfuse, LangSmith), cost tracking, alerts, trace analysis.
  Use when user says "add tracing", "observability", "Langfuse", "LangSmith", "cost tracking",
  "monitoring", "debug agent run", "alerts", "OpenTelemetry", "trace my agent".
  Do NOT use for deployment (use deploying-ai-systems) or testing (use testing-ai-systems).
---
# Instrumenting Observability

Add tracing, cost tracking, alerting, and trace analysis to AI systems.

## Instructions

### Step 1: Identify observability needs
Ask or infer what the user needs:
- LLM call tracing → Step 2
- Cost tracking / budgets → `references/cost-tracking.md`
- Alerts (latency, errors, cost) → `references/alert-configs.md`
- Embedding drift / analysis → `references/phoenix-setup.md`

### Step 2: Choose observability platform
Read the relevant reference based on user preference or stack:
- **Langfuse** (default, self-hostable, open-source) → `references/langfuse-setup.md`
- **LangSmith** (LangChain/LangGraph users) → `references/langsmith-setup.md`
- **Arize Phoenix** (embedding analysis, drift) → `references/phoenix-setup.md`

Decision guide:
| Criterion | Langfuse | LangSmith | Phoenix |
|---|---|---|---|
| Self-host | Yes (Docker) | No (cloud) | Yes (local) |
| LangChain native | Via callback | Zero-config | Via callback |
| LiteLLM native | Built-in callback | Manual | Manual |
| Prompt versioning | Yes | Yes (Hub) | No |
| Embedding analysis | No | No | Yes |
| Cost tracking | Built-in | Built-in | No |

### Step 3: Instrument code
Follow the chosen reference to add instrumentation:
1. Install dependencies
2. Set environment variables
3. Add decorators / callbacks to agent code
4. Tag traces with metadata (user_id, session_id, model)

### Step 4: Setup alerts
Read `references/alert-configs.md`. Configure:
- Latency threshold alerts
- Error rate monitoring
- Cost spike detection
- Notification channels (Slack, email)

### Step 5: Verify traces
Run the agent and confirm:
- Traces appear in the dashboard
- Token counts and costs are recorded
- Nested spans show tool calls and LLM invocations
- Metadata tags are attached correctly

## Quick Verification
```python
# Langfuse: check trace exists
from langfuse import Langfuse
client = Langfuse()
traces = client.fetch_traces(limit=1)
print(f"Latest trace: {traces.data[0].id}")

# LangSmith: check via CLI
# langsmith traces list --limit 1
```

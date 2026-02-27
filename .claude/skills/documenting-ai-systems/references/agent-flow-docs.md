# Agent Flow Documentation

## Template

```markdown
# Agent: [Name]

## Purpose
[One sentence: what this agent does]

## Complexity Level
[Level N from complexity ladder + justification]

## Flow Diagram
[Mermaid flowchart showing the agent's decision/execution flow]

## Inputs
| Input | Type | Source | Required |
|-------|------|--------|----------|
| user_message | string | API request | Yes |
| session_id | string | API request | No |

## Outputs
| Output | Type | Description |
|--------|------|-------------|
| response | string | Agent's answer |
| sources | list[str] | Referenced documents |

## Tools Used
| Tool | Risk | Description |
|------|------|-------------|
| search_docs | read-only | Search knowledge base |
| create_ticket | reversible | Create support ticket |

## State Machine
[Mermaid stateDiagram if stateful]

## Error Handling
| Error | Recovery |
|-------|----------|
| LLM timeout | Retry with fallback model |
| Tool failure | Return partial result with error note |

## Dependencies
- LLM: gpt-4o via LiteLLM
- Vector DB: Qdrant on port 6333
- Cache: Redis on port 6379

## Observability
- Traces: Langfuse (all LLM calls traced)
- Metrics: tokens/request, latency P50/P95, cost/request
- Alerts: error rate > 5%, latency P95 > 10s
```

## Multi-Agent System Doc

Add sections for:
- **Agent Roster**: table of all agents with roles
- **Handoff Protocol**: what context is passed between agents
- **Communication Diagram**: Mermaid sequence diagram showing agent interactions

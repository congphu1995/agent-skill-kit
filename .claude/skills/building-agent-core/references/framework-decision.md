# Framework Decision Tree

Choose the simplest framework that meets requirements.

## Decision Tree

```
Do you need any framework at all?
├─ Simple chatbot / single-turn / no state → Raw LiteLLM API
├─ Need structured output + type safety → PydanticAI
├─ Need stateful workflows / HITL / branching → LangGraph
├─ Need role-based multi-agent with minimal code → CrewAI
└─ Building on OpenAI ecosystem with handoffs → OpenAI Agents SDK
```

## Framework Comparison

| Feature | Raw LiteLLM | PydanticAI | LangGraph | CrewAI | OpenAI Agents SDK |
|---------|-------------|------------|-----------|--------|-------------------|
| Learning curve | Lowest | Low | Medium | Low | Low |
| Structured output | Via Instructor | Native | Manual | Built-in | Auto schema |
| State management | Manual | No | Checkpointers | Session | No |
| Multi-agent | Manual | No | Subgraphs | Native (crews) | Handoffs |
| HITL | Manual | No | interrupt() | No | No |
| Streaming | Yes | Yes | Yes | Limited | Yes |
| Provider agnostic | Yes (100+) | Yes | Yes (via LiteLLM) | Yes | OpenAI only |

## When to Use Each

### Raw LiteLLM API (Default)
- Simple chatbot or Q&A
- Single-turn classification/generation
- Prototyping and experimentation
- Maximum flexibility needed

### PydanticAI
- Structured output is primary need
- Type safety and validation critical
- Dependency injection pattern fits
- Don't need state management

### LangGraph
- Multi-step workflows with branching
- Human-in-the-loop required
- Need checkpointing / resumability
- Complex state machines
- Production stateful agents

### CrewAI
- Role-based agents (researcher, writer, reviewer)
- Want quick setup with minimal code
- Sequential or hierarchical task execution
- Don't need fine-grained control

### OpenAI Agents SDK
- Committed to OpenAI ecosystem
- Need triage → specialist handoff pattern
- Want built-in guardrail primitives
- MCP integration needed

## Rule
**Start with Raw LiteLLM. Upgrade only when you hit a limitation the framework solves.**

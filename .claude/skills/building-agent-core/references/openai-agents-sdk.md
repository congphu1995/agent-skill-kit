# OpenAI Agents SDK Patterns

> Stub — expand after first project using extracting-patterns (F2)

## Quick Start

```bash
pip install openai-agents
```

## Key Concepts

- **Agent**: name, instructions, tools — the core primitive
- **Handoff**: transfer control between agents with context
- **Guardrail**: input/output validation on agent responses

## Basic Example

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
)

result = Runner.run_sync(agent, "What is the capital of France?")
print(result.final_output)
```

## Triage Pattern

```python
from agents import Agent, Runner

billing_agent = Agent(name="Billing", instructions="Handle billing questions.")
tech_agent = Agent(name="Technical", instructions="Handle technical questions.")

triage_agent = Agent(
    name="Triage",
    instructions="Route to billing or technical agent based on the question.",
    handoffs=[billing_agent, tech_agent],
)

result = Runner.run_sync(triage_agent, "I was charged twice")
# Automatically hands off to billing_agent
```

## MCP Integration
The SDK supports MCP servers as tool providers for agents.

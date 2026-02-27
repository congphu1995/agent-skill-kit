---
name: building-agent-core
description: >
  Build AI agents: LLM integration via LiteLLM, tool calling, memory, multi-agent, streaming, guardrails.
  Use when user says "build agent", "LLM integration", "tool calling", "function calling", "agent memory",
  "multi-agent", "connect to OpenAI/Anthropic/Ollama", "LangGraph", "CrewAI", "guardrails", "safety rails",
  "human-in-the-loop", "LiteLLM", "chatbot", "assistant", "conversational AI".
  Do NOT use for RAG/embeddings/vector search (use building-rag-pipeline).
  Do NOT use for designing agent architecture (use designing-agent-system).
---
# Building Agent Core

Generate agent code: LLM integration, tool calling, memory, multi-agent, streaming, guardrails.

## Instructions

### Step 1: Check for design doc
Look for `.claude/artifacts/designing-agent-system-*.md`. If exists, follow its specifications.
If not, ask: "Do you want to design the agent architecture first? (`/designing-agent-system`)"

### Step 2: Determine framework
Read `references/framework-decision.md`. Choose based on requirements:
- Simple chatbot/single-turn → raw LiteLLM (default)
- Need structured output → PydanticAI
- Need state/HITL/branching → LangGraph
- Need role-based multi-agent → CrewAI
- OpenAI ecosystem → OpenAI Agents SDK

### Step 3: Setup LLM client
Read `references/llm-integration.md`. Minimal LiteLLM setup:

```python
import litellm
from dotenv import load_dotenv

load_dotenv()

response = litellm.completion(
    model="anthropic/claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello"}],
    # Fallback chain for reliability
    fallbacks=[{"model": "openai/gpt-4o"}],
)
```

Configure: provider selection, fallback chains, cost optimization (caching, model routing).

### Step 4: Implement core agent
Based on framework choice, read the relevant reference:
- Raw API: `references/tool-calling.md`
- LangGraph: `references/langgraph-patterns.md`
- CrewAI: `references/crewai-patterns.md`
- OpenAI Agents SDK: `references/openai-agents-sdk.md`

Minimal agent loop (raw API):

```python
import litellm, json

tools = [{"type": "function", "function": {
    "name": "search", "description": "Search the web",
    "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
}}]

messages = [{"role": "system", "content": "You are a helpful assistant."}]

def agent_loop(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})
    while True:
        response = litellm.completion(model="anthropic/claude-sonnet-4-20250514", messages=messages, tools=tools)
        msg = response.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content
        for tc in msg.tool_calls:
            result = execute_tool(tc.function.name, json.loads(tc.function.arguments))
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
```

### Step 5: Add capabilities (as needed)
- Memory → `references/memory-patterns.md`
- Multi-agent → `references/multi-agent.md`
- Streaming → `references/streaming.md`

### Step 6: Add guardrails
Read `references/guardrails-patterns.md`. Always include:
- Input validation (prompt injection detection)
- Output validation (format checking, hallucination guard)
- Tool risk enforcement (confirm before irreversible actions)

# LangGraph / LangChain Agent Template

## Directory Structure
```
<project-name>/
  src/
    __init__.py
    agents/__init__.py, graph.py, nodes.py, state.py
    tools/__init__.py
    rag/__init__.py
    models/schemas.py
    checkpointing/store.py
  tests/unit/, integration/, conftest.py
  evals/datasets/, eval_runner.py
  scripts/run_agent.py
  .env.example, pyproject.toml, Dockerfile, langgraph.json
```

## pyproject.toml
```toml
[project]
name = "<project-name>"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "langgraph>=0.2",
    "langchain-core>=0.3",
    "langchain-openai>=0.2",
    "langchain-anthropic>=0.3",
    "langgraph-checkpoint-sqlite>=2.0",
    "pydantic>=2.9",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.24", "ruff>=0.8"]
rag = ["chromadb>=0.5", "langchain-chroma>=0.2"]
```

## src/agents/state.py
```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    context: str
    next_step: str
```

## src/agents/graph.py
```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from src.agents.state import AgentState
from src.agents.nodes import route, call_llm, use_tool

builder = StateGraph(AgentState)
builder.add_node("llm", call_llm)
builder.add_node("tool", use_tool)
builder.set_entry_point("llm")
builder.add_conditional_edges("llm", route, {"tool": "tool", "end": END})
builder.add_edge("tool", "llm")
memory = SqliteSaver.from_conn_string(":memory:")
graph = builder.compile(checkpointer=memory)
```

## .env.example / langgraph.json
```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
CHECKPOINT_DB=checkpoints.db
```
```json
{"graphs": {"agent": "./src/agents/graph.py:graph"}, "env": ".env"}
```

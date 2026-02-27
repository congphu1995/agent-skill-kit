# LangSmith Setup

LangChain's observability platform. Zero-config for LangChain/LangGraph, manual tracing for others.

## Environment Variables

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY="lsv2_pt_..."
export LANGCHAIN_PROJECT="my-agent"  # optional, defaults to "default"
```

## Zero-Config for LangChain / LangGraph

```python
# Just set env vars above -- all LangChain calls are traced automatically
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke([HumanMessage(content="Hello")])  # fully traced
```

## LangGraph Auto-Tracing

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    query: str
    result: str

def process(state: State) -> State:
    return {"result": f"Processed: {state['query']}"}

graph = StateGraph(State)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
app = graph.compile()
# Full graph execution traced automatically
result = app.invoke({"query": "test"})
```

## Manual Tracing with @traceable

For non-LangChain code or custom functions:

```python
from langsmith import traceable
import litellm

@traceable(name="my-agent", tags=["production"])
def my_agent(query: str) -> str:
    context = retrieve(query)
    return generate(query, context)

@traceable
def retrieve(query: str) -> str:
    """Child span under my-agent."""
    return "relevant context"

@traceable(metadata={"model": "gpt-4o-mini"})
def generate(query: str, context: str) -> str:
    response = litellm.completion(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
    )
    return response.choices[0].message.content

# Traces appear at https://smith.langchain.com
result = my_agent("What is AI?")
```

## Trace Visualization

LangSmith dashboard shows:
- **Trace waterfall**: nested spans with timing for each step
- **Token counts**: input/output tokens per LLM call
- **Latency breakdown**: time spent in each node/tool
- **Run tree**: parent-child relationships between spans

## Filtering and Quick Verification

```python
from langsmith import Client
client = Client()
runs = client.list_runs(
    project_name="my-agent",
    filter='eq(status, "error")',
    limit=10,
)
for run in runs:
    print(f"{run.name}: {run.status} ({run.total_tokens} tokens)")
```

```bash
langsmith traces list --project "my-agent" --limit 5
```

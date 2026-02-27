# Multi-Agent Patterns

When and how to split an agent into multiple agents.

## When to Split

| Signal | Action |
|--------|--------|
| Agent needs >50 tools | Split by domain |
| Agent needs different system prompts for subtasks | Specialist agents |
| Different tasks need different models | Route to appropriate model |
| Need error isolation | Separate failure domains |
| Need different security boundaries | Isolate PII-handling agents |

## Supervisor Pattern (LangGraph)

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]
    next_agent: str

def supervisor(state: State) -> dict:
    response = completion(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a supervisor. Route to:
            - researcher: for finding information
            - writer: for creating content
            - FINISH: when task is complete"""},
            *state["messages"]
        ]
    )
    return {"next_agent": response.choices[0].message.content.strip()}

def researcher(state: State) -> dict:
    response = completion(model="gpt-4o", messages=[
        {"role": "system", "content": "You are a research specialist."},
        *state["messages"]
    ])
    return {"messages": [{"role": "assistant", "content": f"[Research]: {response.choices[0].message.content}"}]}

def writer(state: State) -> dict:
    response = completion(model="gpt-4o", messages=[
        {"role": "system", "content": "You are a writing specialist."},
        *state["messages"]
    ])
    return {"messages": [{"role": "assistant", "content": f"[Writer]: {response.choices[0].message.content}"}]}

def route(state: State) -> str:
    if "FINISH" in state["next_agent"]:
        return END
    elif "researcher" in state["next_agent"].lower():
        return "researcher"
    return "writer"

graph = StateGraph(State)
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges("supervisor", route, {
    "researcher": "researcher", "writer": "writer", END: END
})
graph.add_edge("researcher", "supervisor")
graph.add_edge("writer", "supervisor")

app = graph.compile()
```

## Handoff Pattern

```python
def handoff(from_agent: str, to_agent: str, context: dict):
    return {
        "messages": [{
            "role": "system",
            "content": f"Handoff from {from_agent}. Context: {json.dumps(context)}"
        }],
        "next_agent": to_agent
    }
```

## Communication Best Practices
- **Shared state**: all agents read/write to common TypedDict (LangGraph default)
- **Message passing**: agents communicate via messages in state
- **Keep handoffs minimal**: pass only what the next agent needs
- **Log all transitions**: for debugging and observability

## Anti-Patterns
- **Over-splitting**: 10 agents for a task that needs 2
- **Circular dependencies**: Agent A calls B calls A
- **No termination**: supervisor never returns FINISH
- **State bloat**: every agent appends to messages without cleanup

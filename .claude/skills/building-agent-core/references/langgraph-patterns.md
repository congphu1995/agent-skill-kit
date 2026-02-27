# LangGraph Patterns

Stateful agent workflows with LangGraph.

## Installation

```bash
pip install langgraph langgraph-checkpoint-postgres litellm
```

## Full Working Example: Tool-Calling Agent

```python
from typing import TypedDict, Annotated
from operator import add
from litellm import completion
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import json

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[list, add]

# 2. Define Tools
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
}]

def execute_tool(name: str, args: dict) -> str:
    if name == "get_weather":
        return json.dumps({"city": args["city"], "temp": "22C", "condition": "sunny"})
    return json.dumps({"error": f"Unknown tool: {name}"})

# 3. Define Nodes
def agent_node(state: AgentState) -> dict:
    response = completion(model="gpt-4o", messages=state["messages"], tools=tools)
    return {"messages": [response.choices[0].message]}

def tool_node(state: AgentState) -> dict:
    last_message = state["messages"][-1]
    results = []
    for tc in last_message.tool_calls:
        result = execute_tool(tc.function.name, json.loads(tc.function.arguments))
        results.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    return {"messages": results}

# 4. Define Routing
def should_continue(state: AgentState) -> str:
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END

# 5. Build Graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

# 6. Compile with Checkpointer
app = graph.compile(checkpointer=MemorySaver())

# 7. Run
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Tokyo?"}]},
    config
)
print(result["messages"][-1].content)
```

## State Design

```python
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]    # Append-only (reducer: add)
    current_step: str                  # Overwrite (no reducer)
    collected_data: Annotated[dict, merge_dicts]  # Custom reducer

def merge_dicts(a: dict, b: dict) -> dict:
    return {**a, **b}
```

## Conditional Edges

```python
def route_by_intent(state):
    intent = state["messages"][-1].content
    if "billing" in intent.lower():
        return "billing_agent"
    elif "technical" in intent.lower():
        return "tech_agent"
    return "general_agent"

graph.add_conditional_edges("classifier", route_by_intent, {
    "billing_agent": "billing",
    "tech_agent": "technical",
    "general_agent": "general"
})
```

## Checkpointers

```python
# Development
from langgraph.checkpoint.memory import MemorySaver
app = graph.compile(checkpointer=MemorySaver())

# Production
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver.from_conn_string("postgresql://user:pass@host/db")
app = graph.compile(checkpointer=checkpointer)
```

## Human-in-the-Loop

```python
from langgraph.types import interrupt, Command

def approval_node(state):
    decision = interrupt({
        "message": "Approve this action?",
        "data": state["pending_action"]
    })
    return {"approved": decision == "yes"}

# Resume after human input
app.invoke(Command(resume="yes"), config)
```

## Subgraphs

```python
# Define inner graph
inner = StateGraph(InnerState)
inner.add_node(...)
inner_app = inner.compile()

# Use as node in outer graph
outer = StateGraph(OuterState)
outer.add_node("sub_agent", inner_app)
```

## Thread Management (Multi-Session)

```python
# Each user gets their own thread
config_user_1 = {"configurable": {"thread_id": "user-1"}}
config_user_2 = {"configurable": {"thread_id": "user-2"}}

# State is isolated per thread
app.invoke({"messages": [msg]}, config_user_1)
app.invoke({"messages": [msg]}, config_user_2)
```

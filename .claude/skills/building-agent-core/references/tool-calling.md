# Tool Calling Patterns

Cross-framework tool calling with LiteLLM.

## Define Tools

```python
import json
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="Search query")
    max_results: int = Field(5, ge=1, le=20, description="Number of results")

tools = [{
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "Search the knowledge base for relevant documents",
        "parameters": SearchInput.model_json_schema()
    }
}]
```

## Tool Execution Loop

```python
from litellm import completion

def run_agent(user_message: str, tools: list, tool_functions: dict):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]

    while True:
        response = completion(model="gpt-4o", messages=messages, tools=tools)
        msg = response.choices[0].message
        messages.append(msg)

        # No tool calls — return final response
        if not msg.tool_calls:
            return msg.content

        # Execute each tool call
        for tc in msg.tool_calls:
            func_name = tc.function.name
            func_args = json.loads(tc.function.arguments)

            try:
                result = tool_functions[func_name](**func_args)
                tool_result = json.dumps(result, default=str)
            except Exception as e:
                tool_result = json.dumps({"error": str(e)})

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": tool_result
            })

# Usage
tool_functions = {
    "search_documents": lambda query, max_results=5: [{"title": "Doc 1", "score": 0.9}],
}
result = run_agent("Find docs about authentication", tools, tool_functions)
```

## Parallel Tool Calls

Some models return multiple tool calls in a single response. Handle all of them:

```python
for tc in msg.tool_calls:  # May be 1 or many
    result = tool_functions[tc.function.name](**json.loads(tc.function.arguments))
    messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})
```

## Tool Choice

```python
# Let model decide (default)
response = completion(model="gpt-4o", messages=messages, tools=tools)

# Force a specific tool
response = completion(model="gpt-4o", messages=messages, tools=tools,
                      tool_choice={"type": "function", "function": {"name": "search_documents"}})

# Force no tools
response = completion(model="gpt-4o", messages=messages, tools=tools,
                      tool_choice="none")
```

## Error Handling

```python
def safe_execute(func_name: str, func_args: dict, tool_functions: dict) -> str:
    if func_name not in tool_functions:
        return json.dumps({"error": f"Unknown tool: {func_name}. Available: {list(tool_functions.keys())}"})
    try:
        result = tool_functions[func_name](**func_args)
        return json.dumps(result, default=str)
    except TypeError as e:
        return json.dumps({"error": f"Invalid arguments: {e}"})
    except Exception as e:
        return json.dumps({"error": f"{type(e).__name__}: {e}"})
```

## Max Iterations Safety

```python
MAX_ITERATIONS = 10

for i in range(MAX_ITERATIONS):
    response = completion(model="gpt-4o", messages=messages, tools=tools)
    msg = response.choices[0].message
    messages.append(msg)
    if not msg.tool_calls:
        break
    # ... execute tools ...
else:
    return "Agent reached maximum iterations without completing."
```

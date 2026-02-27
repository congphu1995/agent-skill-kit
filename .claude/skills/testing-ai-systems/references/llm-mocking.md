# LLM Mocking Patterns

## Why Mock LLM Calls

- **Deterministic tests**: Same input always produces same output
- **No API costs**: Tests run without burning tokens
- **Fast execution**: No network latency, tests run in milliseconds
- **Offline-capable**: CI/CD pipelines don't need API keys

## Response Factory

Create realistic LLM response objects that match the OpenAI/LiteLLM structure.

```python
from unittest.mock import MagicMock

def make_completion_response(content, tool_calls=None):
    """Factory for mock LLM responses."""
    message = MagicMock()
    message.content = content
    message.tool_calls = tool_calls
    response = MagicMock()
    response.choices = [MagicMock(message=message)]
    response.usage = MagicMock(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    return response

def make_tool_call(name, arguments):
    """Factory for mock tool calls."""
    tool_call = MagicMock()
    tool_call.id = "call_abc123"
    tool_call.type = "function"
    tool_call.function = MagicMock()
    tool_call.function.name = name
    tool_call.function.arguments = json.dumps(arguments)
    return tool_call

def make_tool_call_response(tool_name, tool_args):
    """Factory for LLM response that requests a tool call."""
    tc = make_tool_call(tool_name, tool_args)
    return make_completion_response(content=None, tool_calls=[tc])
```

## unittest.mock Approach

Patch the completion function at the call site.

```python
from unittest.mock import patch

@patch("litellm.completion")
def test_agent_classifies_ticket(mock_completion):
    mock_completion.return_value = make_completion_response("billing")
    result = classify_ticket("I was charged twice")
    assert result == "billing"
    mock_completion.assert_called_once()
```

Verify prompt construction:

```python
@patch("litellm.completion")
def test_system_prompt_included(mock_completion):
    mock_completion.return_value = make_completion_response("ok")
    classify_ticket("test input")
    call_args = mock_completion.call_args
    messages = call_args.kwargs["messages"]
    assert messages[0]["role"] == "system"
    assert "classify" in messages[0]["content"].lower()
```

## pytest-mock Approach

Use the `mocker` fixture for cleaner syntax.

```python
def test_agent_summarizes(mocker):
    mock = mocker.patch("myapp.agent.litellm.completion")
    mock.return_value = make_completion_response("Summary: key points here")
    result = summarize("Long document text...")
    assert "key points" in result
```

## Fixture Patterns

Define reusable fixtures in `conftest.py`.

```python
import pytest

@pytest.fixture
def mock_llm(mocker):
    """Patch litellm.completion and return the mock."""
    return mocker.patch("myapp.agent.litellm.completion")

@pytest.fixture
def billing_response():
    return make_completion_response("billing")

@pytest.fixture
def refund_tool_call():
    return make_tool_call_response("process_refund", {"amount": 29.99})

def test_billing_classification(mock_llm, billing_response):
    mock_llm.return_value = billing_response
    assert classify_ticket("charged twice") == "billing"
```

## Tool Call Mocking

Test that the agent correctly handles tool call responses from the LLM.

```python
@patch("litellm.completion")
def test_agent_calls_search_tool(mock_completion):
    mock_completion.return_value = make_tool_call_response(
        "search", {"query": "Python testing"}
    )
    state = {"messages": [{"role": "user", "content": "How do I test Python?"}]}
    result = agent_node(state)
    tool_call = result["messages"][-1].tool_calls[0]
    assert tool_call.function.name == "search"

@patch("litellm.completion")
def test_agent_handles_multiple_tool_calls(mock_completion):
    tc1 = make_tool_call("search", {"query": "weather"})
    tc2 = make_tool_call("calendar", {"date": "today"})
    mock_completion.return_value = make_completion_response(None, tool_calls=[tc1, tc2])
    state = {"messages": [{"role": "user", "content": "What's the weather for my meeting?"}]}
    result = agent_node(state)
    names = [tc.function.name for tc in result["messages"][-1].tool_calls]
    assert "search" in names
    assert "calendar" in names
```

## Streaming Mocking

Mock streaming responses by returning an iterable of chunks.

```python
def make_stream_chunks(content_parts):
    """Factory for mock streaming response."""
    for part in content_parts:
        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta = MagicMock()
        chunk.choices[0].delta.content = part
        chunk.choices[0].delta.tool_calls = None
        yield chunk

@patch("litellm.completion")
def test_streaming_agent(mock_completion):
    mock_completion.return_value = make_stream_chunks(["Hello", " world", "!"])
    result = stream_response("Say hello")
    assert result == "Hello world!"
```

## Common Pitfalls

- **Patch at the call site**, not the definition site: `@patch("myapp.agent.litellm.completion")`, not `@patch("litellm.completion")` (unless your code imports litellm directly)
- **Match the return type**: If your code calls `response.choices[0].message.content`, your mock must have that same structure
- **Mock side_effect for sequences**: Use `mock.side_effect = [resp1, resp2]` for multi-turn conversations
- **Don't forget error cases**: `mock.side_effect = Exception("API timeout")` to test error handling

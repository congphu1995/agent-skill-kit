# MCP Server Testing

## MCP Inspector

Use the official inspector for interactive testing during development.

```bash
npx @modelcontextprotocol/inspector
```

The inspector connects to your MCP server and lets you:
- List available tools and their schemas
- Call tools with sample inputs and inspect responses
- Verify error handling behavior

## Unit Testing Tool Handlers

Test each tool handler as a standalone function.

```python
import pytest
from myapp.mcp_server import handle_search, handle_create_item

def test_search_tool_returns_results():
    result = handle_search({"query": "Python testing", "limit": 5})
    assert isinstance(result, list)
    assert len(result) <= 5
    assert all("title" in item for item in result)

def test_search_tool_empty_query():
    with pytest.raises(ValueError, match="query cannot be empty"):
        handle_search({"query": "", "limit": 5})

def test_create_item_returns_id():
    result = handle_create_item({"name": "Test Item", "description": "A test"})
    assert "id" in result
    assert isinstance(result["id"], str)
```

## Integration Testing

Test the full flow: tool request -> handler -> external API -> response.

```python
@patch("myapp.mcp_server.api_client.search")
def test_search_tool_calls_api(mock_api):
    mock_api.return_value = [{"id": "1", "title": "Result"}]
    result = handle_search({"query": "test", "limit": 10})
    assert result == [{"id": "1", "title": "Result"}]
    mock_api.assert_called_once_with(query="test", limit=10)

@patch("myapp.mcp_server.api_client.create")
def test_create_tool_handles_api_error(mock_api):
    mock_api.side_effect = ConnectionError("API unreachable")
    with pytest.raises(Exception, match="API unreachable"):
        handle_create_item({"name": "Test"})
```

## Schema Validation

Verify tool input/output schemas match expectations.

```python
from jsonschema import validate, ValidationError

def test_search_input_schema():
    schema = get_tool_schema("search")["inputSchema"]
    # Valid input passes
    validate({"query": "test", "limit": 5}, schema)
    # Missing required field fails
    with pytest.raises(ValidationError):
        validate({"limit": 5}, schema)

def test_search_output_matches_schema():
    result = handle_search({"query": "test", "limit": 5})
    output_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["title"],
            "properties": {"title": {"type": "string"}},
        },
    }
    validate(result, output_schema)
```

## Error Handling Tests

```python
def test_invalid_tool_name():
    """Server should return error for unknown tool."""
    result = dispatch_tool("nonexistent_tool", {})
    assert result["isError"] is True

def test_tool_timeout(mocker):
    """Tool should handle timeout gracefully."""
    mocker.patch("myapp.mcp_server.api_client.search", side_effect=TimeoutError)
    result = handle_search_safe({"query": "slow query", "limit": 5})
    assert result["isError"] is True
    assert "timeout" in result["message"].lower()

def test_malformed_input():
    """Tool should reject input that doesn't match schema."""
    with pytest.raises((ValueError, ValidationError)):
        handle_search({"query": 123})  # query should be string
```

## Testing with mcp-proxy

Use `mcp-proxy` to test your server with real MCP clients.

```bash
# Start your MCP server
python -m myapp.mcp_server &

# Connect via mcp-proxy for client-side testing
npx mcp-proxy --server stdio --command "python -m myapp.mcp_server"
```

## Test Organization for MCP Servers

```
tests/
├── test_tool_handlers.py      # Unit tests for each tool handler
├── test_tool_schemas.py       # Schema validation tests
├── test_tool_integration.py   # Integration tests with mocked APIs
└── conftest.py                # Shared fixtures, mock API responses
```

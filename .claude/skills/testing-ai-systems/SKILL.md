---
name: testing-ai-systems
description: >
  Write tests for AI systems: unit tests with LLM mocking, integration tests, agent behavior tests,
  MCP server tests. Use when user says "write tests", "test agent", "unit test", "integration test",
  "test MCP", "mock LLM", "test my AI code", "agent testing".
  Do NOT use for prompt evaluation/benchmarking (use evaluating-and-benchmarking).
  Do NOT use for code review (use reviewing-ai-code).
---

# Testing AI Systems

Test AI code using TDD adapted for non-deterministic systems.

## Workflow

1. **Identify test scope** — unit, integration, or end-to-end?
2. **Identify AI-specific concerns** — What needs mocking? LLM calls? External APIs? Vector DB?
3. **Write tests following TDD** — Red-green-refactor cycle
4. **Use appropriate mocking strategy** — Read `references/llm-mocking.md`
5. **Test agent behavior** — Read `references/agent-behavior-testing.md`
6. **Test MCP servers** — Read `references/mcp-testing.md` if applicable

## Core TDD Principles

### Red-Green-Refactor

1. Write a failing test that describes expected behavior
2. Write the minimum code to make the test pass
3. Refactor while keeping all tests green

### Test Quality Rules

- One behavior per test, clear descriptive names
- Prefer real code over mocks — mock only LLM calls and external services
- Use deterministic assertions (exact match on mocked outputs, structural checks on real outputs)
- Test error paths: API failures, malformed responses, timeouts, rate limits

### What to Mock vs What to Keep Real

| Mock | Keep Real |
|------|-----------|
| LLM API calls (litellm, openai) | Prompt formatting / template logic |
| External APIs (search, DB) | Tool implementations (parsers, calculators) |
| Vector DB queries | State management / graph transitions |
| Embedding calls | Input validation and output parsing |

## Test Organization

```
tests/
├── unit/              # Individual functions, tools, prompt formatting
├── integration/       # Agent + tools together (mocked LLM, real tools)
├── e2e/               # Full agent loop (may use real LLM, mark slow)
└── conftest.py        # Shared fixtures: mock responses, test data
```

## Quick Reference

- **Mocking LLM calls**: See `references/llm-mocking.md` for patterns, factories, streaming
- **Agent behavior**: See `references/agent-behavior-testing.md` for state transitions, multi-turn, tool selection
- **MCP servers**: See `references/mcp-testing.md` for inspector, tool handler tests, schema validation

## Common Fixtures

```python
# conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_llm_response():
    """Reusable mock LLM response factory."""
    def _make(content, tool_calls=None):
        message = MagicMock()
        message.content = content
        message.tool_calls = tool_calls
        response = MagicMock()
        response.choices = [MagicMock(message=message)]
        return response
    return _make
```

## Checklist Before Submitting Tests

- [ ] All tests pass with `pytest -v`
- [ ] LLM calls are mocked (no real API calls in unit/integration tests)
- [ ] Error cases covered (malformed LLM response, API timeout, invalid tool input)
- [ ] Test names describe behavior, not implementation
- [ ] No flaky tests — deterministic assertions on mocked outputs

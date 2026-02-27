# AI Code Anti-Patterns

Common anti-patterns in AI/agent codebases. For each, the pattern is described, why it is problematic, and what to do instead.

---

## 1. God Agent

**Pattern**: A single agent that handles every task — routing, retrieval, computation, output formatting, error handling — all in one monolithic prompt and loop.

**Why it's bad**: Prompts become unmanageable. The agent performs poorly on specialized tasks because its attention is split. Debugging is nearly impossible.

**Fix**: Split into specialized agents with clear responsibilities. Use a router/orchestrator to delegate. Each agent should do one thing well.

---

## 2. Context Stuffing

**Pattern**: Cramming everything into the system prompt — all documentation, all examples, all rules, all edge cases — hoping the model will "just figure it out."

**Why it's bad**: Exceeds context windows, wastes tokens, degrades performance on the actual task due to attention dilution. The model pays equal attention to irrelevant context.

**Fix**: Use retrieval (RAG) to inject only relevant context. Keep the system prompt focused on identity, behavior rules, and output format. Load examples dynamically.

---

## 3. Blind Tool Trust

**Pattern**: Executing tool results without any validation. The agent calls a tool, gets a result, and passes it directly to the user or into the next step.

**Why it's bad**: Tool results can be malformed, contain injected instructions, or return unexpected data types. This is a primary vector for indirect prompt injection.

**Fix**: Validate tool outputs against expected schemas. Sanitize text results before including them in prompts. Never execute code returned by tools without sandboxing.

---

## 4. Missing Error Recovery

**Pattern**: No fallback when the LLM returns garbage, refuses to answer, hits rate limits, or produces malformed output. The system just crashes or hangs.

**Why it's bad**: LLMs are non-deterministic. They will fail. Production systems without error recovery are unreliable.

**Fix**: Implement retry with backoff. Parse and validate LLM output. Have fallback responses for common failure modes. Use structured output (JSON mode, tool_use) to reduce parse failures. Set timeouts.

---

## 5. Hardcoded Prompts

**Pattern**: Prompts embedded as string literals deep inside application code, mixed with business logic.

**Why it's bad**: Cannot A/B test prompts. Cannot update prompts without redeploying. Cannot track which prompt version produced which output. Makes prompt review difficult.

**Fix**: Externalize prompts into template files or a prompt management system. Version prompts. Log which prompt version was used for each request. Treat prompts as configuration, not code.

---

## 6. No Observability

**Pattern**: No logging of LLM calls, no cost tracking, no latency monitoring, no tracing of agent decision paths.

**Why it's bad**: Cannot debug production issues. Cannot track costs. Cannot identify which prompts or tools are underperforming. Flying blind.

**Fix**: Log every LLM call with: model, prompt hash, token counts, latency, cost. Use tracing (LangSmith, Braintrust, or custom) for multi-step agents. Set up cost alerts.

---

## 7. Synchronous Everything

**Pattern**: Making all LLM calls sequentially, even when they are independent of each other. Blocking the main thread on every API call.

**Why it's bad**: LLM calls take 1-30 seconds. Sequential calls multiply latency. Users wait unnecessarily.

**Fix**: Identify independent calls and run them in parallel (asyncio.gather, Promise.all). Use streaming for user-facing responses. Offload long-running agent tasks to background workers.

---

## 8. No Rate Limiting

**Pattern**: Allowing unlimited LLM calls per user, per session, or per time window. No circuit breakers.

**Why it's bad**: A single user or a bug can burn through your entire API budget. Agentic loops can spin indefinitely. No protection against abuse.

**Fix**: Implement per-user and per-session rate limits. Set max iterations on agentic loops. Add circuit breakers that stop after N consecutive failures. Set budget caps per request.

---

## 9. Missing Guardrails

**Pattern**: No input validation before sending to the LLM. No output checking before returning to the user. Raw user input concatenated into prompts.

**Why it's bad**: Prompt injection, data leakage, harmful outputs. The LLM becomes an unfiltered pipe between the user and your system.

**Fix**: Validate and sanitize user inputs. Use content moderation on outputs. Separate user input from system instructions. Implement output filters for PII, code injection, and harmful content.

---

## 10. Framework Overuse

**Pattern**: Using LangChain/LangGraph/CrewAI/AutoGen for a simple chatbot or a single-tool agent. Adding layers of abstraction that provide no value for the use case.

**Why it's bad**: Adds complexity, dependencies, and debugging difficulty. Framework abstractions hide what is actually happening. Simple problems get buried under unnecessary orchestration.

**Fix**: Start with direct API calls (Anthropic SDK, OpenAI SDK). Add a framework only when you have multiple agents, complex routing, or state management needs that justify the overhead. Match framework complexity to problem complexity.

---

## Quick Reference

| Anti-Pattern | Severity | Detection Signal |
|---|---|---|
| God Agent | High | System prompt > 2000 tokens, agent handles 5+ distinct tasks |
| Context Stuffing | Medium | System prompt > 8000 tokens, includes raw docs |
| Blind Tool Trust | Critical | No validation between tool output and next LLM call |
| Missing Error Recovery | High | No try/catch around LLM calls, no retries |
| Hardcoded Prompts | Medium | String literals with LLM instructions in .py/.ts files |
| No Observability | Medium | No logging library, no cost tracking code |
| Synchronous Everything | Medium | Sequential await/await pattern on independent calls |
| No Rate Limiting | High | No rate limit middleware, no loop bounds |
| Missing Guardrails | Critical | User input directly in f-strings/template literals |
| Framework Overuse | Low | Heavy framework imports for < 3 tools or single agent |

# Cost Optimization for AI Systems

Strategies to reduce LLM API costs without sacrificing quality.

---

## 1. Model Selection

Use the cheapest model that meets quality requirements for each task.

| Task Type | Recommended Tier | Examples |
|-----------|-----------------|----------|
| Classification, routing, extraction | Small/fast | Haiku, GPT-4o-mini, Gemini Flash |
| Summarization, generation, analysis | Mid-tier | Sonnet, GPT-4o |
| Complex reasoning, coding, research | Large | Opus, o1/o3, Gemini Pro |

**Rule of thumb**: Start with the smallest model. Move up only when quality metrics demand it.

---

## 2. Prompt Caching

Cache system prompts and repeated context to avoid re-processing.

- **Anthropic prompt caching**: Automatically caches system prompt prefix. Reduces cost by up to 90% on cached tokens.
- **LiteLLM / custom cache**: Cache full request-response pairs keyed on prompt hash. Good for deterministic queries.
- **Semantic cache**: Cache based on input similarity (embedding distance). Good for FAQ-style queries.

**Estimated savings**: 60-90% on repeated system prompts, 30-50% on similar queries.

---

## 3. Token Reduction

Every token costs money. Reduce input and output tokens.

### Input tokens
- Keep system prompts concise (under 1500 tokens for most tasks).
- Summarize conversation history instead of sending full transcripts.
- Use RAG to inject only relevant context, not entire documents.
- Remove redundant instructions and examples from prompts.

### Output tokens
- Set `max_tokens` to a reasonable limit for the task.
- Use structured output (JSON, tool_use) to get concise responses.
- Ask for specific formats: "Reply in 1-2 sentences" vs. open-ended.
- Use `stop_sequences` to terminate output early when possible.

**Estimated savings**: 20-40% from prompt optimization alone.

---

## 4. Batching

Group similar requests to reduce overhead and improve throughput.

- **Anthropic Message Batches API**: Submit up to 10,000 requests at 50% cost reduction. Results within 24 hours.
- **Application-level batching**: Collect multiple user requests and process together.
- **Batch classification**: Classify multiple items in a single prompt instead of one-per-call.

**Estimated savings**: 50% with batch APIs, variable with application-level batching.

---

## 5. Rate Limiting & Budget Controls

Prevent cost overruns before they happen.

- Set per-user request limits (e.g., 100 requests/hour for free tier).
- Set per-session token budgets (e.g., max 50K tokens per conversation).
- Set per-request cost ceilings (abort if estimated cost exceeds threshold).
- Implement circuit breakers: stop after N consecutive failures to avoid retry storms.
- Set monthly budget alerts at 50%, 80%, and 100% of target spend.

---

## 6. Cost Tracking

You cannot optimize what you do not measure.

- Log per-request: model, input tokens, output tokens, cached tokens, cost.
- Aggregate per-user: daily/monthly spend per user or user tier.
- Aggregate per-feature: which features consume the most tokens.
- Track cost-per-outcome: cost per successful task completion, not just per API call.
- Dashboard: real-time cost monitoring with anomaly alerts.

### Cost calculation

```
cost = (input_tokens * input_price / 1M) + (output_tokens * output_price / 1M)
     - (cached_tokens * cache_discount / 1M)
```

---

## 7. Model Routing

Route requests to the right model based on task complexity.

```
Simple query (< 50 tokens, classification) -> Haiku / GPT-4o-mini
Medium query (generation, summarization)   -> Sonnet / GPT-4o
Complex query (multi-step reasoning, code) -> Opus / o3
```

Implementation approaches:
- **Rule-based**: Route by task type, input length, or feature flag.
- **Classifier-based**: Use a small model to classify complexity, then route.
- **Cascade**: Try small model first; escalate to larger model if confidence is low.

**Estimated savings**: 40-60% compared to using the largest model for everything.

---

## Savings Summary

| Strategy | Estimated Savings | Implementation Effort |
|----------|------------------|-----------------------|
| Prompt caching | 60-90% on cached portions | Low |
| Model routing | 40-60% overall | Medium |
| Batch API | 50% on batch-eligible work | Low |
| Token reduction | 20-40% | Low-Medium |
| Rate limiting | Prevents overruns | Low |
| Cost tracking | Enables optimization | Medium |

**Combined potential**: 50-80% cost reduction compared to naive implementation.

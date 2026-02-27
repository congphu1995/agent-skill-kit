# Benchmark Sources

## LLM Leaderboards

| Leaderboard | URL | Focus |
|-------------|-----|-------|
| LMSYS Chatbot Arena | lmarena.ai | Human preference ranking |
| Hugging Face Open LLM | huggingface.co/spaces/open-llm-leaderboard | Open-source models |
| Artificial Analysis | artificialanalysis.ai | Speed, cost, quality combined |
| LiveBench | livebench.ai | Contamination-free benchmarks |

## Embedding Benchmarks

| Benchmark | Focus |
|-----------|-------|
| MTEB | Massive Text Embedding Benchmark — multilingual |
| BEIR | Retrieval benchmark across domains |

## Key Metrics to Compare

### Quality
- Task-specific accuracy (classification, generation, retrieval)
- Human preference (Elo rating from LMSYS)
- Domain-specific benchmarks (medical, legal, code)

### Cost
- Input token price (per 1M tokens)
- Output token price (per 1M tokens)
- Prompt caching discount
- Batch API pricing

### Speed
- Time to first token (TTFT)
- Tokens per second (throughput)
- P50 and P95 latency

## Benchmark Report Template

```markdown
# Benchmark: [Topic]

## Models Tested
| Model | Provider | Price (input/output per 1M) |
|-------|----------|----------------------------|

## Results
| Model | Quality Score | Latency P50 | Cost/1K requests |
|-------|--------------|-------------|------------------|

## Analysis
[Key findings and trade-offs]

## Recommendation
[Best model for this use case + justification]
```

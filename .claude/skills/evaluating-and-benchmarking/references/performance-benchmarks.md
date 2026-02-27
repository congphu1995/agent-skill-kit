# Performance Benchmarks

> Stub -- expand after first project using extracting-patterns (F2)

## Metrics

| Metric | Description | How to Measure |
|--------|-------------|----------------|
| Task completion rate | % of tasks the agent completes successfully | End-to-end eval with pass/fail assertions |
| Tool accuracy | Correct tool selection % | Log tool calls, compare to ground truth sequences |
| Hallucination rate | % of outputs containing fabricated information | LLM-as-judge or human review on sampled outputs |
| Cost per task | Total tokens x price per token | Track token usage per request via provider API |
| Latency P50 | Median response time | Instrument API calls with timing |
| Latency P95 | 95th percentile response time | Identify slow outliers |
| Latency P99 | 99th percentile response time | Worst-case user experience |

## Benchmarking Methodology

1. **Define the task set** -- 50+ representative tasks with known correct outputs
2. **Control variables** -- Same prompts, same temperature (0), same test environment
3. **Run multiple trials** -- At least 3 runs per configuration to account for variance
4. **Record all dimensions** -- Accuracy alone is insufficient; track cost and latency too
5. **Compare against baseline** -- Always compare to a known-good configuration

## Cost Estimation Formula

```
Cost per task = (input_tokens * input_price + output_tokens * output_price) * avg_calls_per_task
```

Example for a 3-step agent task using Claude Sonnet:
```
= (1000 * $0.003/1K + 500 * $0.015/1K) * 3 calls
= ($0.003 + $0.0075) * 3
= $0.0315 per task
```

## Tracking Over Time

- Log every eval run with timestamp, git SHA, model version, and results
- Plot accuracy, cost, and latency trends on a dashboard
- Set alerts for regressions beyond acceptable thresholds
- Store raw results in JSON for historical comparison

# Three-Tier Eval Strategy

Evals should run at three levels: fast checks on every PR, comprehensive nightly suites, and continuous production monitoring. Each tier serves a different purpose.

---

## Tier 1: PR Gates

**Goal:** Catch obvious regressions before merge. Fast enough to run on every pull request.

- **10-20 core test cases** covering the most critical behaviors
- **Execution time:** < 2 minutes
- **Blocking:** PR cannot merge if any assertion fails
- **Scope:** Exact-match and contains assertions only (no LLM-as-judge, too slow/expensive)

```yaml
# promptfooconfig.pr-gate.yaml
description: "PR gate eval -- core cases only"
providers:
  - id: anthropic:messages:claude-sonnet-4-20250514
prompts:
  - file://prompts/classify.txt
tests: file://evals/datasets/pr-gate-core.json
```

### GitHub Actions Example

```yaml
# .github/workflows/eval-pr-gate.yml
name: "Eval: PR Gate"
on: [pull_request]

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Run PR gate eval
        run: npx promptfoo@latest eval -c promptfooconfig.pr-gate.yaml --ci
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## Tier 2: Nightly Regression

**Goal:** Comprehensive quality assessment. Catches subtle regressions and tracks quality trends.

- **50+ test cases** across all categories (happy path, edge, adversarial, regression)
- **Execution time:** 5-15 minutes
- **Non-blocking:** Results posted to Slack or dashboard, not gating deploys
- **Scope:** Full assertion types including LLM-as-judge, semantic similarity, model comparison

```yaml
# promptfooconfig.nightly.yaml
description: "Nightly full regression eval"
providers:
  - id: openai:gpt-4o
  - id: anthropic:messages:claude-sonnet-4-20250514
prompts:
  - file://prompts/classify.txt
tests: file://evals/datasets/full-regression.json
```

### GitHub Actions Example

```yaml
# .github/workflows/eval-nightly.yml
name: "Eval: Nightly Regression"
on:
  schedule:
    - cron: "0 2 * * *"  # 2 AM daily

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Run nightly eval
        run: npx promptfoo@latest eval -c promptfooconfig.nightly.yaml -o results.json
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - name: Post results to Slack
        if: always()
        run: |
          PASS=$(jq '.results.stats.successes' results.json)
          TOTAL=$(jq '.results.stats.count' results.json)
          curl -X POST "${{ secrets.SLACK_WEBHOOK }}" \
            -d "{\"text\": \"Nightly eval: ${PASS}/${TOTAL} passed\"}"
```

---

## Tier 3: Production Monitoring

**Goal:** Detect quality degradation in real traffic. Catches issues that synthetic evals miss.

- **Every production request** is logged with input, output, latency, and cost
- **Sampled evaluation:** 1-5% of requests are evaluated by LLM-as-judge
- **Alerting:** Slack/PagerDuty alert when quality drops below threshold
- **Tools:** Langfuse, LangSmith, Braintrust, or custom logging

### Key Metrics to Track

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Task completion rate | > 90% | Warn at 85%, page at 80% |
| Hallucination rate | < 5% | Warn at 8%, page at 10% |
| Avg latency (P95) | < 5s | Warn at 8s, page at 15s |
| Cost per request | < $0.05 | Warn at $0.08 |
| User feedback (thumbs up) | > 80% | Warn at 70% |

### Langfuse Integration Example

```python
from langfuse import Langfuse

langfuse = Langfuse()

trace = langfuse.trace(name="classify-ticket")
generation = trace.generation(
    name="classification",
    input=ticket_text,
    output=classification_result,
    model="claude-sonnet-4-20250514",
    usage={"input": prompt_tokens, "output": completion_tokens},
)
trace.score(name="correct", value=1.0 if is_correct else 0.0)
```

---

## Summary

| Tier | When | Cases | Speed | Blocking | Assertions |
|------|------|-------|-------|----------|------------|
| PR gate | Every PR | 10-20 | < 2 min | Yes | Exact, contains |
| Nightly | Daily | 50+ | 5-15 min | No | All (incl. LLM judge) |
| Production | Continuous | All traffic | Real-time | Alerting | Sampled LLM judge |

---
name: evaluating-and-benchmarking
description: >
  Evaluate and benchmark AI agents and prompts using promptfoo, DeepEval, and custom eval frameworks.
  Use when user says "evaluate prompt", "eval pipeline", "benchmark", "red team", "adversarial test",
  "promptfoo", "DeepEval", "eval dataset", "regression test", "CI eval gate", "test my prompts",
  "measure agent quality", "compare models".
  Do NOT use for unit/integration tests (use testing-ai-systems).
  Do NOT use for code review (use reviewing-ai-code).
---

# Evaluating and Benchmarking AI Systems

## Core Principle

**Create evals BEFORE building.** If you don't have evals, you don't have a product. Evals are the test suite for AI -- they tell you whether your system is improving or regressing with every change.

---

## Process

### Step 1: Identify Eval Type

Determine what you are evaluating:
- **Prompt eval** -- Does this prompt produce correct, consistent output?
- **Agent eval** -- Does the agent use the right tools and complete tasks?
- **RAG eval** -- Are retrieved documents relevant? Are answers faithful to context?
- **Model comparison** -- Which model performs best for this task at what cost?

### Step 2: Generate Test Dataset

Read `references/eval-dataset-generation.md`. Create 20-50 real-world test cases covering:
- Happy path (40%), edge cases (30%), adversarial (20%), regression (10%)
- Each case: input, expected_output, category, difficulty

### Step 3: Setup Eval Framework

Choose framework based on eval type:
- **Prompt/model eval** -- Read `references/promptfoo-setup.md`. Use promptfoo for assertion-based eval with model comparison.
- **Agent eval** -- Read `references/deepeval-setup.md`. Use DeepEval for multi-step agent evaluation with semantic metrics.
- **Security eval** -- Read `references/red-teaming.md`. Use Garak or PyRIT for adversarial testing.
- **Performance tracking** -- Read `references/performance-benchmarks.md`. Track latency, cost, and accuracy.

Minimal promptfoo config:

```yaml
# promptfooconfig.yaml
prompts:
  - "You are a helpful assistant. User: {{query}}"

providers:
  - id: anthropic:messages:claude-sonnet-4-20250514
  - id: openai:gpt-4o

tests:
  - vars:
      query: "What is the capital of France?"
    assert:
      - type: contains
        value: "Paris"
      - type: llm-rubric
        value: "Answer is factually correct and concise"
  - vars:
      query: "Explain quantum computing in one sentence"
    assert:
      - type: llm-rubric
        value: "Explanation is accurate and understandable"
```

Run with: `npx promptfoo@latest eval`

### Step 4: Configure Eval Tiers

Read `references/three-tier-eval.md`. Set up a tiered evaluation strategy:
- **Tier 1: PR gates** -- 10-20 core cases, block merge on regression
- **Tier 2: Nightly regression** -- 50+ cases, full model comparison
- **Tier 3: Production monitoring** -- Live quality tracking, alerts on degradation

### Step 5: Run and Iterate

1. Run the eval suite: `npx promptfoo eval` or `deepeval test run`
2. Analyze failures -- are they prompt issues, data issues, or model limitations?
3. Fix the root cause, re-run evals, confirm improvement
4. Never "fix" evals by weakening assertions -- fix the system instead

### Step 6: Output Artifact

Write results summary to `.claude/artifacts/evaluating-{name}.md` including:
- Eval type and framework used
- Dataset size and category breakdown
- Pass/fail rates per category
- Model comparison results (if applicable)
- Recommended next steps

---

## Anti-Patterns

- Evaluating with < 20 test cases -- you will miss failure modes
- Exact-match only assertions -- use semantic similarity and LLM-as-judge
- Skipping adversarial cases -- your users will find the edge cases you didn't test
- Running evals only locally -- evals must run in CI to catch regressions
- Testing with synthetic data only -- sample real user inputs when possible

---

## Reference Files

- [Promptfoo Setup](references/promptfoo-setup.md) -- Complete promptfoo configuration and usage
- [Eval Dataset Generation](references/eval-dataset-generation.md) -- Building high-quality test datasets
- [Three-Tier Eval Strategy](references/three-tier-eval.md) -- PR gates, nightly, production monitoring
- [DeepEval Setup](references/deepeval-setup.md) -- Agent evaluation with semantic metrics (stub)
- [Red-Teaming](references/red-teaming.md) -- Adversarial testing tools and frameworks (stub)
- [Performance Benchmarks](references/performance-benchmarks.md) -- Latency, cost, accuracy tracking (stub)

## Checklist
- [ ] Eval dataset has 20+ test cases
- [ ] Happy path, edge cases, and adversarial cases covered
- [ ] Eval runs in CI (PR gate at minimum)
- [ ] Assertions use semantic checks, not just exact match
- [ ] Results artifact written with pass/fail breakdown

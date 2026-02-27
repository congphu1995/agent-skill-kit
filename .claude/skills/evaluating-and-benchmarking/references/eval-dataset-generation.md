# Eval Dataset Generation

A high-quality eval dataset is the foundation of reliable AI evaluation. Poor datasets lead to false confidence -- your system appears to work until it fails in production.

---

## Minimum Requirements

- **20-50 test cases** for any eval (fewer gives unreliable signal)
- **Balanced categories** to cover the full input space
- **Human-reviewed** -- never ship an eval dataset without human verification

---

## Category Distribution

| Category | % of Dataset | Purpose |
|----------|-------------|---------|
| Happy path | 40% | Common, expected inputs that must always work |
| Edge cases | 30% | Boundary conditions, unusual formats, ambiguous inputs |
| Adversarial | 20% | Prompt injection, jailbreaks, malformed inputs |
| Regression | 10% | Previously broken cases -- these must never regress |

---

## Test Case Template

Each test case should follow this structure:

```json
{
  "id": "TC-001",
  "input": "I was charged twice for my subscription last month",
  "expected_output": "billing",
  "category": "happy_path",
  "difficulty": "easy",
  "tags": ["billing", "duplicate-charge"],
  "notes": "Clear billing issue, single category"
}
```

### Fields

- **id** -- Unique identifier for tracking regressions
- **input** -- The exact input to the system under test
- **expected_output** -- The correct output (exact match, semantic, or rubric)
- **category** -- happy_path, edge_case, adversarial, or regression
- **difficulty** -- easy, medium, hard (helps prioritize fixes)
- **tags** -- Searchable labels for filtering
- **notes** -- Why this case exists, what it tests

---

## Generating Test Cases with LLMs

Use an LLM to bootstrap your dataset, then review manually:

```
Generate 20 realistic support tickets for a SaaS billing system.
Include a mix of:
- 8 clear, straightforward billing issues
- 6 edge cases (e.g., tickets that mention billing but are really technical)
- 4 adversarial inputs (e.g., prompt injection attempts, gibberish)
- 2 regression cases based on these known failures: [paste failures]

For each case, provide:
- input: the ticket text
- expected_output: the correct category
- category: happy_path | edge_case | adversarial | regression
- difficulty: easy | medium | hard
- reasoning: why this expected_output is correct

Output as JSON array.
```

**Critical: always human-review generated datasets.** LLMs will generate plausible-looking but subtly wrong expected outputs. Review every single case.

---

## Sampling Real-World Data

The best eval data comes from production:

1. **Sample recent inputs** -- Pull 100 random inputs from your logs
2. **Label manually** -- Have a human assign the correct output to each
3. **Filter for diversity** -- Remove near-duplicates, keep representative spread
4. **Add hard cases** -- Production data skews toward happy path; add edge cases manually
5. **Anonymize** -- Strip PII before committing to version control

---

## Dataset Versioning

Treat eval datasets like code:

```
evals/
  datasets/
    classification_v1.json       # Initial dataset
    classification_v2.json       # Added edge cases after prod failure
    classification_v3.json       # Added adversarial cases after red-team
  CHANGELOG.md                   # Document what changed and why
```

Version control rules:
- **Never delete test cases** -- move them to a "retired" section with a reason
- **Never weaken assertions** to make tests pass -- fix the system instead
- **Document additions** -- every new case should reference the failure or gap it addresses
- **Review dataset changes in PRs** -- treat dataset changes as seriously as code changes

---

## Dataset Quality Checklist

Before using a dataset for evaluation:

- [ ] At least 20 test cases
- [ ] All four categories represented (happy, edge, adversarial, regression)
- [ ] Every expected_output verified by a human
- [ ] No duplicate or near-duplicate inputs
- [ ] Adversarial cases include prompt injection attempts
- [ ] Edge cases cover format variations (typos, casing, empty input)
- [ ] Regression cases reference the original failure
- [ ] Dataset is committed to version control
- [ ] PII is removed from any production-sourced data

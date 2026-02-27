# DeepEval Setup

> Stub -- expand after first project using extracting-patterns (F2)

## Quick Start

```bash
pip install deepeval
```

## Key Concepts

- **pytest-like syntax:** `assert_test(test_case, [metric])` -- integrates naturally with existing Python test suites
- **50+ metrics:** faithfulness, answer relevancy, hallucination, toxicity, bias, contextual precision/recall
- **Agent evaluation:** Track tool call sequences, verify correct tool selection, measure multi-step task completion
- **RAG evaluation:** Dedicated metrics for retrieval quality (contextual relevancy, faithfulness to retrieved docs)

## Basic Usage

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

test_case = LLMTestCase(
    input="What is the refund policy?",
    actual_output="Our refund policy allows returns within 30 days.",
    retrieval_context=["Refund policy: 30-day return window for all purchases."]
)

metric = AnswerRelevancyMetric(threshold=0.7)
assert_test(test_case, [metric])
```

## Running Evals

```bash
deepeval test run test_eval.py          # Run all eval tests
deepeval test run test_eval.py --verbose # Verbose output with metric scores
```

## When to Use DeepEval vs Promptfoo

- **Promptfoo** -- Best for prompt iteration, model comparison, and CI gates with deterministic assertions
- **DeepEval** -- Best for agent/RAG evaluation with semantic metrics, Python-native workflows

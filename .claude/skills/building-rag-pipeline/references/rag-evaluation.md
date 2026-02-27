# RAG Evaluation

Measure RAG quality with RAGAS metrics before deploying.

## RAGAS Metrics

| Metric | Measures | Range | Target |
|--------|----------|-------|--------|
| **Faithfulness** | Is the answer grounded in the context? | 0-1 | > 0.8 |
| **Answer Relevancy** | Does the answer address the question? | 0-1 | > 0.8 |
| **Context Precision** | Are retrieved chunks relevant? | 0-1 | > 0.7 |
| **Context Recall** | Were all needed chunks retrieved? | 0-1 | > 0.7 |

## Quick Setup

```bash
pip install ragas datasets
```

## Running Evaluation

```python
from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

samples = [
    SingleTurnSample(
        user_input="What is the capital of France?",
        retrieved_contexts=["France is a country in Europe. Its capital is Paris."],
        response="The capital of France is Paris.",
        reference="Paris is the capital of France."
    ),
]
dataset = EvaluationDataset(samples=samples)
results = evaluate(dataset=dataset,
                   metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
print(results)  # {'faithfulness': 0.95, 'answer_relevancy': 0.92, ...}
```

## Evaluating Your RAG Pipeline

```python
from ragas import SingleTurnSample, EvaluationDataset, evaluate
from ragas.metrics import faithfulness, answer_relevancy

def evaluate_rag_pipeline(rag_fn, test_cases: list[dict]) -> dict:
    """rag_fn(query) -> {"answer": str, "contexts": list[str]}"""
    samples = []
    for case in test_cases:
        result = rag_fn(case["query"])
        samples.append(SingleTurnSample(
            user_input=case["query"], retrieved_contexts=result["contexts"],
            response=result["answer"], reference=case["reference"]
        ))
    return evaluate(EvaluationDataset(samples=samples), metrics=[faithfulness, answer_relevancy])

scores = evaluate_rag_pipeline(my_rag_fn, [{"query": "Refund policy?", "reference": "30-day full refund."}])
```

## Integration with promptfoo (CI)

```yaml
# promptfoo.yaml
providers:
  - id: python:rag_pipeline.py
prompts:
  - "{{query}}"
tests:
  - vars:
      query: "What is the return policy?"
    assert:
      - type: python
        value: "output['faithfulness'] > 0.8"
      - type: python
        value: "output['answer_relevancy'] > 0.8"
```

```bash
# Run in CI
npx promptfoo eval --config promptfoo.yaml
```

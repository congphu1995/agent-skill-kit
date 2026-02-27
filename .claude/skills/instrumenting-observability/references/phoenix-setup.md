# Arize Phoenix Setup

Open-source embedding analysis, drift detection, and LLM trace visualization.

## Installation

```bash
pip install arize-phoenix opentelemetry-api opentelemetry-sdk
```

## Local Launch

```python
import phoenix as px
session = px.launch_app()  # http://localhost:6006
```

Or: `phoenix serve`

## LLM Tracing with OpenTelemetry

```python
from phoenix.otel import register
from openinference.instrumentation.litellm import LiteLLMInstrumentor
import litellm

tracer_provider = register(project_name="my-agent")
LiteLLMInstrumentor().instrument(tracer_provider=tracer_provider)

# All LiteLLM calls now traced in Phoenix
response = litellm.completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
)
```

## Embedding Drift Detection

```python
import phoenix as px
import pandas as pd

prod_df = pd.DataFrame({
    "embedding": [emb1, emb2, ...],
    "text": ["query1", "query2", ...],
})
ref_df = pd.DataFrame({
    "embedding": [ref1, ref2, ...],
    "text": ["ref1", "ref2", ...],
})

session = px.launch_app(
    primary=px.Inferences(prod_df, "production"),
    reference=px.Inferences(ref_df, "reference"),
)
# UI shows: drift metrics, cluster analysis, outlier detection
```

## RAG Retrieval Analysis

```python
from phoenix.evals import HallucinationEvaluator, QAEvaluator, OpenAIModel

eval_model = OpenAIModel(model="gpt-4o-mini")
hallucination_eval = HallucinationEvaluator(eval_model)
qa_eval = QAEvaluator(eval_model)

from phoenix.evals import run_evals
results = run_evals(
    dataframe=rag_results_df,  # needs query, context, response columns
    evaluators=[hallucination_eval, qa_eval],
)
```

## Quick Verification

```bash
phoenix serve &
curl -s http://localhost:6006/healthz  # should return OK
```

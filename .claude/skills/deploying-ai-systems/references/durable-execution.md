# Durable Execution

Long-running agent workflows that survive failures.

## When Needed
- Workflows taking minutes/hours (not seconds)
- Must survive server restarts
- Need exactly-once execution guarantees
- Complex retry and compensation logic

## Temporal (Mission-Critical)

```python
# pip install temporalio
from temporalio import workflow, activity
from datetime import timedelta

@activity.defn
async def process_claim(claim_id: str) -> dict:
    """Long-running LLM processing."""
    result = await completion(model="gpt-4o", messages=[...])
    return {"claim_id": claim_id, "decision": result}

@workflow.defn
class ClaimWorkflow:
    @workflow.run
    async def run(self, claim_id: str):
        result = await workflow.execute_activity(
            process_claim, claim_id,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(maximum_attempts=3)
        )
        return result
```

**Use for**: insurance claims, financial workflows, multi-step approval processes.

## LangGraph Checkpointers (Lightweight)

```python
from langgraph.checkpoint.postgres import PostgresSaver
# See building-agent-core/references/langgraph-patterns.md
```

**Use for**: stateful agents with HITL, conversation persistence.

## Inngest (Serverless)

```python
# pip install inngest
import inngest

@inngest.create_function(
    fn_id="process-document",
    trigger=inngest.TriggerEvent(event="document/uploaded"),
)
async def process_document(ctx, step):
    chunks = await step.run("chunk", chunk_document, ctx.event.data["doc_id"])
    embeddings = await step.run("embed", embed_chunks, chunks)
    await step.run("index", index_embeddings, embeddings)
```

**Use for**: event-driven workflows, serverless environments.

## Decision

| Requirement | Solution |
|-------------|----------|
| Mission-critical, exactly-once | Temporal |
| Stateful agent with checkpoints | LangGraph + PostgresSaver |
| Serverless, event-driven | Inngest |
| Simple retry logic | Python tenacity library |

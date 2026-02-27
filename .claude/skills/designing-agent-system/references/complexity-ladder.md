# Complexity Ladder

Anthropic's principle: **start simple, escalate only when needed.** Try level N before level N+1.

## Levels

### Level 1: Single LLM Call

One prompt, one response. No chaining, no tools.

**Use when:**
- Task is straightforward classification, generation, or transformation
- Input and output are well-defined
- No external data needed beyond what fits in the prompt

**Examples:** Sentiment analysis, text summarization, translation, code review comments, email drafting.

**Techniques:** Prompt engineering, few-shot examples, system prompt tuning.

---

### Level 2: Prompt Chaining

Sequential LLM calls where output of one feeds the next. Gate between steps validates intermediate results.

**Use when:**
- Task has clear decomposable steps
- Each step benefits from focused instructions
- Intermediate validation improves reliability

**Examples:** Generate outline -> write draft -> review for errors -> produce final. Extract data -> validate -> format.

**Pattern:**
```
Input -> LLM Step 1 -> Gate/Validate -> LLM Step 2 -> Gate/Validate -> Output
```

---

### Level 3: Routing

Classify input first, then route to a specialized prompt or handler.

**Use when:**
- Inputs vary widely in type or intent
- Different inputs need different handling strategies
- A single prompt cannot handle all variations well

**Examples:** Support ticket -> billing / technical / general. Document -> contract / invoice / letter.

**Pattern:**
```
Input -> Classifier LLM -> Route A (specialized prompt)
                        -> Route B (specialized prompt)
                        -> Route C (specialized prompt)
```

---

### Level 4: Parallelization

Run multiple LLM calls concurrently on the same input, then aggregate.

**Use when:**
- Task has independent subtasks that can run simultaneously
- Multiple perspectives or analyses are needed
- Latency matters and steps are not dependent

**Variants:**
- **Sectioning**: split task into independent parts, run in parallel, combine
- **Voting**: run same prompt N times, take majority or best result

**Examples:** Analyze document for legal + financial + technical risks in parallel. Generate 3 candidate responses, pick best.

---

### Level 5: Orchestrator-Workers

Central orchestrator LLM dynamically plans subtasks and delegates to worker LLMs.

**Use when:**
- Task requires dynamic planning (subtasks not known upfront)
- Workers need different tools or specializations
- Complex multi-step execution with adaptive flow

**Examples:** Research agent that plans queries, dispatches searches, synthesizes. Coding agent that plans changes across multiple files.

**Pattern:**
```
Input -> Orchestrator (plans subtasks)
           -> Worker 1 (executes subtask)
           -> Worker 2 (executes subtask)
         Orchestrator (synthesizes results) -> Output
```

---

### Level 6: Evaluator-Optimizer

Generate output, evaluate it, improve in a loop until quality threshold is met.

**Use when:**
- Output quality requires iterative refinement
- Clear evaluation criteria exist
- Single-pass output is not good enough

**Examples:** Code generation -> test -> fix errors -> re-test. Essay writing -> critique -> revise.

**Pattern:**
```
Input -> Generator LLM -> Evaluator LLM -> [meets bar?]
                              |                  |
                              No (feedback)      Yes -> Output
                              |
                              v
                          Generator LLM (retry with feedback)
```

---

### Level 7: Autonomous Agent

LLM in a loop: observe environment, decide next action, execute with tools, repeat until goal is met.

**Use when:**
- Task is open-ended and requires exploration
- Number of steps is not predictable
- Agent must adapt based on intermediate results
- Environment interaction is required

**Examples:** Bug investigation, data analysis with follow-up questions, web research with dynamic queries.

**Guardrails required:** Max iterations, cost caps, human-in-the-loop checkpoints, sandboxed execution.

---

## Decision Flowchart

```
START: Can a single well-crafted prompt solve this?
  |
  Yes -> Level 1
  |
  No -> Can the task be broken into fixed sequential steps?
          |
          Yes -> Level 2 (Prompt Chaining)
          |
          No -> Do inputs vary and need different handling?
                  |
                  Yes -> Level 3 (Routing)
                  |
                  No -> Are there independent subtasks to run simultaneously?
                          |
                          Yes -> Level 4 (Parallelization)
                          |
                          No -> Does the task require dynamic planning?
                                  |
                                  Yes -> Level 5 (Orchestrator-Workers)
                                  |
                                  No -> Does output need iterative refinement?
                                          |
                                          Yes -> Level 6 (Evaluator-Optimizer)
                                          |
                                          No -> Is the task open-ended with unknown steps?
                                                  |
                                                  Yes -> Level 7 (Autonomous Agent)
                                                  |
                                                  No -> Revisit Level 1 with better prompting
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Jumping to multi-agent for a classification task | Use Level 1 with few-shot examples |
| Building orchestrator for a 3-step pipeline | Use Level 2 prompt chaining |
| Using autonomous agent for structured data extraction | Use Level 1 with structured output |
| No guardrails on Level 7 agents | Add max iterations, cost caps, HITL |
| Over-engineering routing when one prompt works | Benchmark single prompt first |

## Rule

**Always start at the lowest level that meets requirements. Document why you chose level N and why level N-1 is insufficient.**

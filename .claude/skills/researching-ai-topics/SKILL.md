---
name: researching-ai-topics
description: >
  Research AI topics: paper search, framework comparison, benchmark analysis, competitive analysis, model evaluation.
  Use when user says "research", "compare frameworks", "which model", "find papers", "competitive analysis",
  "benchmark comparison", "what's the best", "latest in AI", "compare LLMs", "model comparison".
  Do NOT use for designing agent architecture (use designing-agent-system) or building agents (use building-agent-core).
context: fork
---
# Researching AI Topics

Structured research on AI topics with sourced analysis.

## Instructions

### Step 1: Clarify research question
- What specific question needs answering?
- What decisions will this research inform?
- What depth is needed? (quick comparison vs deep dive)

### Step 2: Identify research type
- **Paper search** → `references/paper-search.md`
- **Framework comparison** → `references/framework-comparison-template.md`
- **Benchmark analysis** → `references/benchmark-sources.md`

### Step 3: Gather information
- Search the web for recent publications, benchmarks, documentation
- Read official documentation and changelogs
- Check benchmark leaderboards (LMSYS, Hugging Face Open LLM)
- Compare pricing pages for cost analysis

### Step 4: Analyze and structure
Use this comparison table format:

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| **Primary use case** | | | |
| **Strengths** | | | |
| **Weaknesses** | | | |
| **Pricing** | | | |
| **Maturity** | | | |
| **Community/ecosystem** | | | |
| **Verdict** | | | |

Guidelines:
- Always include trade-offs (cost vs quality, speed vs accuracy, flexibility vs simplicity)
- Highlight what's most relevant to the user's specific use case
- Cite sources for all claims with URLs
- For LLM comparisons, include: context window, input/output pricing, latency, benchmark scores

### Step 5: Produce artifact
Write to `.claude/artifacts/researching-ai-topics-{topic}.md` with:
- Executive summary (2-3 sentences)
- Detailed comparison (tables, analysis)
- Recommendation with justification
- Sources list

## Checklist
- [ ] Research question clearly defined
- [ ] At least 3 sources consulted
- [ ] Comparison table with consistent criteria
- [ ] Trade-offs explicitly stated
- [ ] All claims cited with URLs
- [ ] Recommendation tied to user's specific context

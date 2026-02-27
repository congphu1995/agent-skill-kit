#!/usr/bin/env python3
"""
Behavioral test suite for Agent Skill Kit.

Tests from "The Complete Guide to Building Skills for Claude" Chapter 3:
  1. Triggering tests — Does each skill load at the right time?
  2. Functional tests — Does the skill produce correct outputs?
  3. Cross-skill routing — Do ambiguous prompts route correctly?

Run: python3 test_skills_behavioral.py
"""

import re
import yaml
import sys
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field

SKILLS_DIR = Path(__file__).parent.parent / ".claude" / "skills"

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
WARN = "\033[93mWARN\033[0m"
INFO = "\033[94mINFO\033[0m"

results = {"pass": 0, "fail": 0, "warn": 0}


def report(status, msg):
    if status == "pass":
        print(f"  {PASS}  {msg}")
        results["pass"] += 1
    elif status == "fail":
        print(f"  {FAIL}  {msg}")
        results["fail"] += 1
    else:
        print(f"  {WARN}  {msg}")
        results["warn"] += 1


def load_all_skills():
    """Load all skill names and descriptions."""
    skills = {}
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text()
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if match:
            try:
                fm = yaml.safe_load(match.group(1))
                skills[skill_dir.name] = {
                    "description": str(fm.get("description", "")),
                    "full_content": content,
                }
            except yaml.YAMLError:
                pass
    return skills


def score_prompt_against_skill(prompt: str, description: str) -> float:
    """
    Score how well a prompt matches a skill description.
    Simulates Claude's skill routing by keyword/phrase matching.
    Returns 0.0-1.0 confidence score.
    """
    prompt_lower = prompt.lower()
    desc_lower = description.lower()

    score = 0.0
    max_possible = 0.0

    # 1. Extract quoted trigger phrases from description
    trigger_phrases = re.findall(r'"([^"]+)"', desc_lower)
    if trigger_phrases:
        phrase_matches = sum(1 for p in trigger_phrases if p in prompt_lower)
        max_possible += 3.0
        score += 3.0 * (phrase_matches / max(len(trigger_phrases), 1))

    # 2. Check "Do NOT use" exclusions — penalty if prompt matches exclusion
    not_use_match = re.search(r"do not use for (.+?)(?:\.|$)", desc_lower)
    if not_use_match:
        exclusion_text = not_use_match.group(1)
        exclusion_words = set(re.findall(r"\b\w{4,}\b", exclusion_text))
        prompt_words = set(re.findall(r"\b\w{4,}\b", prompt_lower))
        overlap = exclusion_words & prompt_words
        if overlap:
            score -= 1.0 * len(overlap)

    # 3. Check first sentence (what the skill does) for topic match
    first_sentence = desc_lower.split(".")[0] if "." in desc_lower else desc_lower[:100]
    key_terms = set(re.findall(r"\b\w{4,}\b", first_sentence))
    prompt_terms = set(re.findall(r"\b\w{4,}\b", prompt_lower))
    topic_overlap = key_terms & prompt_terms
    max_possible += 2.0
    score += 2.0 * min(len(topic_overlap) / max(3, 1), 1.0)

    # Normalize
    if max_possible > 0:
        return max(0.0, min(1.0, score / max_possible))
    return 0.0


def route_prompt(prompt: str, skills: dict) -> list:
    """Route a prompt to skills, return sorted list of (skill, score)."""
    scores = []
    for name, data in skills.items():
        s = score_prompt_against_skill(prompt, data["description"])
        if s > 0.05:
            scores.append((name, s))
    scores.sort(key=lambda x: -x[1])
    return scores


# ============================================================
# TEST SUITE 1: TRIGGERING TESTS
# ============================================================

# For each skill: "should trigger" prompts and "should NOT trigger" prompts
TRIGGER_TEST_CASES = {
    "designing-agent-system": {
        "should_trigger": [
            "Design an agent that can search the web and summarize results",
            "What's the right architecture for a multi-agent customer support system?",
            "Help me design the tools and prompts for my AI assistant",
            "I need a system design for an AI agent that handles refunds",
        ],
        "should_not_trigger": [
            "Write the Python code for my agent",
            "Help me set up my Python environment",
            "What's the weather today?",
        ],
    },
    "building-agent-core": {
        "should_trigger": [
            "Build an agent that uses tool calling to search the web",
            "Help me integrate LiteLLM with my project",
            "Implement a LangGraph agent with memory",
            "Add guardrails to my chatbot",
        ],
        "should_not_trigger": [
            "Build a RAG pipeline with embeddings",
            "Design the architecture for my agent",
            "Write tests for my agent",
        ],
    },
    "building-rag-pipeline": {
        "should_trigger": [
            "Build a RAG pipeline with ChromaDB",
            "Help me chunk documents for vector search",
            "Set up semantic search over my knowledge base",
            "Implement agentic RAG with reranking",
        ],
        "should_not_trigger": [
            "Build a chatbot with tool calling",
            "Deploy my application to Kubernetes",
            "Design an agent architecture",
        ],
    },
    "testing-ai-systems": {
        "should_trigger": [
            "Write unit tests for my agent's tool calling",
            "Help me mock LLM responses in tests",
            "Test my MCP server",
            "Add integration tests for the agent pipeline",
        ],
        "should_not_trigger": [
            "Evaluate my prompts with promptfoo",
            "Review my agent code for security issues",
            "Deploy my AI system",
        ],
    },
    "evaluating-and-benchmarking": {
        "should_trigger": [
            "Set up promptfoo to evaluate my prompts",
            "Create an eval dataset for my agent",
            "Benchmark my agent against GPT-4",
            "Add eval gates to my CI pipeline",
        ],
        "should_not_trigger": [
            "Write pytest unit tests for my code",
            "Build an agent with tool calling",
            "Review my code for bugs",
        ],
    },
    "deploying-ai-systems": {
        "should_trigger": [
            "Create a Dockerfile for my AI service",
            "Set up GitHub Actions CI/CD for my agent",
            "Deploy my agent to Kubernetes",
            "Help me containerize my FastAPI app",
        ],
        "should_not_trigger": [
            "Add Langfuse tracing to my agent",
            "Build the backend API",
            "Write tests for my deployment scripts",
        ],
    },
    "setting-up-ai-dev-env": {
        "should_trigger": [
            "Set up a Python virtual environment for my AI project",
            "Help me install Ollama on my machine",
            "Configure my API keys for OpenAI and Anthropic",
            "Set up GPU and CUDA for local model inference",
        ],
        "should_not_trigger": [
            "Scaffold a new project structure",
            "Build an agent",
            "Deploy my application",
        ],
    },
    "scaffolding-ai-project": {
        "should_trigger": [
            "Scaffold a new AI agent project",
            "Create the project structure for a multi-agent system",
            "Bootstrap a new FastAPI + agent project",
            "Init a new AI project with Docker and CI",
        ],
        "should_not_trigger": [
            "Set up my Python environment",
            "Build the actual agent logic",
            "Deploy the project",
        ],
    },
    "building-mcp-server": {
        "should_trigger": [
            "Build an MCP server for our internal API",
            "Help me create MCP tools in Python with FastMCP",
            "I need an MCP server that connects to Jira",
        ],
        "should_not_trigger": [
            "Build a REST API with FastAPI",
            "Set up a chat interface",
            "Deploy my application",
        ],
    },
    "building-backend-api": {
        "should_trigger": [
            "Build a FastAPI backend for my AI agent",
            "Add streaming SSE endpoint for chat responses",
            "Create a REST API that wraps my agent",
        ],
        "should_not_trigger": [
            "Build a React chat interface",
            "Build an MCP server",
            "Set up my development environment",
        ],
    },
    "building-ai-frontend": {
        "should_trigger": [
            "Build a chat UI for my agent in React",
            "Create a streaming chat interface with Next.js",
            "Build an agent monitoring dashboard",
        ],
        "should_not_trigger": [
            "Build the backend API",
            "Deploy the frontend",
            "Design the agent architecture",
        ],
    },
    "reviewing-ai-code": {
        "should_trigger": [
            "Review my agent code for security issues",
            "Do a safety audit on my prompt handling",
            "Check my code for prompt injection vulnerabilities",
            "Optimize my agent's token costs",
        ],
        "should_not_trigger": [
            "Write tests for my agent",
            "Build an agent",
            "Deploy my AI system",
        ],
    },
    "instrumenting-observability": {
        "should_trigger": [
            "Add Langfuse tracing to my agent",
            "Set up cost tracking for my LLM calls",
            "Help me debug my agent runs with tracing",
            "Configure alerts for my AI pipeline",
        ],
        "should_not_trigger": [
            "Deploy my AI system",
            "Write tests for my agent",
            "Build an agent",
        ],
    },
    "researching-ai-topics": {
        "should_trigger": [
            "Compare LangGraph vs CrewAI for my use case",
            "What's the latest research on RAG optimization?",
            "Which embedding model should I use?",
            "Find papers on agent memory architectures",
        ],
        "should_not_trigger": [
            "Build an agent",
            "Design the agent architecture",
            "Deploy my system",
        ],
    },
    "planning-and-breaking-down": {
        "should_trigger": [
            "Plan the implementation for a customer support agent",
            "Break down this project into tasks",
            "Create an implementation roadmap for my AI product",
        ],
        "should_not_trigger": [
            "Design the agent architecture",
            "Build the agent",
            "Research which framework to use",
        ],
    },
    "documenting-ai-systems": {
        "should_trigger": [
            "Generate API documentation for my agent service",
            "Create an architecture diagram with Mermaid",
            "Write a runbook for the AI system",
            "Document the agent flow and handoffs",
        ],
        "should_not_trigger": [
            "Review my code",
            "Plan the project",
            "Build the documentation site",
        ],
    },
    "creating-and-managing-skills": {
        "should_trigger": [
            "Help me create a new skill for database queries",
            "Build a skill that teaches Claude our deployment process",
            "Update the existing PDF skill",
        ],
        "should_not_trigger": [
            "Build an agent",
            "Deploy my system",
            "Write tests",
        ],
    },
    "extracting-patterns": {
        "should_trigger": [
            "Extract a reusable pattern from what we just built",
            "Save this approach as a skill for future use",
            "What patterns did we use in this session?",
        ],
        "should_not_trigger": [
            "Create a brand new skill from scratch",
            "Build an agent",
            "Review my code",
        ],
    },
}


def test_triggering():
    """Test 1: Triggering — skills route correctly for intended prompts."""
    print("\n" + "=" * 60)
    print("  TEST 1: TRIGGERING")
    print("  Does each skill trigger on the right prompts?")
    print("=" * 60)

    skills = load_all_skills()

    for skill_name, cases in sorted(TRIGGER_TEST_CASES.items()):
        print(f"\n  --- {skill_name} ---")

        # Should trigger tests
        for prompt in cases["should_trigger"]:
            routing = route_prompt(prompt, skills)
            if not routing:
                report("fail", f"SHOULD trigger: \"{prompt[:60]}...\" -> no match")
                continue
            top_skill, top_score = routing[0]
            if top_skill == skill_name:
                report("pass", f"SHOULD trigger: \"{prompt[:50]}...\" -> {top_skill} ({top_score:.2f})")
            else:
                # Check if target skill is in top 3
                top_names = [r[0] for r in routing[:3]]
                if skill_name in top_names:
                    rank = top_names.index(skill_name) + 1
                    report("warn", f"SHOULD trigger: \"{prompt[:50]}...\" -> #{rank} (top was {top_skill})")
                else:
                    report("fail", f"SHOULD trigger: \"{prompt[:50]}...\" -> MISSED (top: {top_skill})")

        # Should NOT trigger tests
        for prompt in cases["should_not_trigger"]:
            routing = route_prompt(prompt, skills)
            if not routing:
                report("pass", f"Should NOT trigger: \"{prompt[:50]}\" -> correct (no match)")
                continue
            top_skill, top_score = routing[0]
            if top_skill == skill_name:
                report("fail", f"Should NOT trigger: \"{prompt[:50]}\" -> WRONGLY matched ({top_score:.2f})")
            else:
                report("pass", f"Should NOT trigger: \"{prompt[:50]}\" -> correct (top: {top_skill})")


# ============================================================
# TEST SUITE 2: FUNCTIONAL TESTS
# ============================================================

@dataclass
class FunctionalTest:
    skill: str
    prompt: str
    expected_steps: list = field(default_factory=list)  # step keywords that should appear
    expected_references: list = field(default_factory=list)  # reference files that should be loaded
    expected_artifact: str = ""  # artifact path pattern
    expected_sections: list = field(default_factory=list)  # sections in output


FUNCTIONAL_TESTS = [
    FunctionalTest(
        skill="designing-agent-system",
        prompt="Design a customer support agent that handles refund requests",
        expected_steps=[
            "requirements",
            "complexity",
            "tools",
            "context",
            "output",
        ],
        expected_references=[
            "complexity-ladder.md",
            "tool-design-patterns.md",
            "context-engineering.md",
        ],
        expected_artifact="designing-agent-system-",
        expected_sections=[
            "Complexity Level",
            "Requirements",
            "Tool Specifications",
        ],
    ),
    FunctionalTest(
        skill="building-agent-core",
        prompt="Build a LangGraph agent with tool calling for web search",
        expected_steps=[
            "design doc",
            "framework",
            "LLM client",
            "agent",
            "guardrails",
        ],
        expected_references=[
            "framework-decision.md",
            "llm-integration.md",
            "langgraph-patterns.md",
        ],
        expected_artifact="",
        expected_sections=[],
    ),
    FunctionalTest(
        skill="testing-ai-systems",
        prompt="Write tests for an agent that uses tool calling",
        expected_steps=[
            "scope",
            "AI-specific",
            "TDD",
            "mock",
        ],
        expected_references=[
            "llm-mocking.md",
            "agent-behavior-testing.md",
        ],
        expected_artifact="",
        expected_sections=[],
    ),
    FunctionalTest(
        skill="deploying-ai-systems",
        prompt="Containerize and deploy my FastAPI agent with CI/CD",
        expected_steps=[
            "target",
            "Dockerfile",
            "CI/CD",
            "secrets",
            "verify",
        ],
        expected_references=[
            "docker-ai-stacks.md",
            "cicd-with-eval-gates.md",
        ],
        expected_artifact="deploying-",
        expected_sections=[],
    ),
    FunctionalTest(
        skill="documenting-ai-systems",
        prompt="Generate architecture documentation with Mermaid diagrams for my agent system",
        expected_steps=[
            "scope",
            "reference",
            "diagram",
            "content",
        ],
        expected_references=[
            "mermaid-patterns.md",
            "agent-flow-docs.md",
        ],
        expected_artifact="documenting-",
        expected_sections=[],
    ),
]


def test_functional():
    """Test 2: Functional — skills contain the right workflow elements."""
    print("\n" + "=" * 60)
    print("  TEST 2: FUNCTIONAL")
    print("  Does each skill define the right workflow for its purpose?")
    print("=" * 60)

    skills = load_all_skills()

    for test in FUNCTIONAL_TESTS:
        print(f"\n  --- {test.skill} ---")
        print(f"  Prompt: \"{test.prompt}\"")

        if test.skill not in skills:
            report("fail", f"{test.skill}: Skill not found")
            continue

        content = skills[test.skill]["full_content"].lower()

        # Check expected workflow steps
        for step_keyword in test.expected_steps:
            if step_keyword.lower() in content:
                report("pass", f"Workflow covers: {step_keyword}")
            else:
                report("fail", f"Workflow MISSING: {step_keyword}")

        # Check reference file routing
        for ref in test.expected_references:
            if ref.lower() in content:
                report("pass", f"References: {ref}")
            else:
                report("fail", f"Reference MISSING: {ref}")

        # Check artifact output
        if test.expected_artifact:
            if test.expected_artifact.lower() in content:
                report("pass", f"Artifact path defined: {test.expected_artifact}*")
            else:
                report("fail", f"Artifact path MISSING: {test.expected_artifact}*")

        # Check output section structure
        for section in test.expected_sections:
            if section.lower() in content:
                report("pass", f"Output section: {section}")
            else:
                report("warn", f"Output section not found: {section}")


# ============================================================
# TEST SUITE 3: CROSS-SKILL ROUTING (AMBIGUOUS PROMPTS)
# ============================================================

AMBIGUOUS_PROMPTS = [
    {
        "prompt": "Help me with my AI agent",
        "description": "Generic - should NOT strongly match any single skill",
        "expected_top": None,  # No single skill should dominate
        "should_be_ambiguous": True,
    },
    {
        "prompt": "I want to build a multi-agent system",
        "description": "Could be design or build - design should come first in workflow",
        "expected_top": "designing-agent-system",
        "should_be_ambiguous": False,
    },
    {
        "prompt": "Test and evaluate my agent's prompt quality",
        "description": "Could be testing or evaluating - eval is about prompt quality",
        "expected_top": "evaluating-and-benchmarking",
        "should_be_ambiguous": False,
    },
    {
        "prompt": "Set up a new agent project with tests and Docker",
        "description": "Scaffolding (project structure) should win over env setup",
        "expected_top": "scaffolding-ai-project",
        "should_be_ambiguous": False,
    },
    {
        "prompt": "Review and improve my agent's architecture",
        "description": "Could be reviewing or designing - review is for existing code",
        "expected_top": "reviewing-ai-code",
        "should_be_ambiguous": False,
    },
    {
        "prompt": "Add vector search to my agent",
        "description": "RAG pipeline, not general agent building",
        "expected_top": "building-rag-pipeline",
        "should_be_ambiguous": False,
    },
    {
        "prompt": "Create a REST API for my chatbot",
        "description": "Backend API, not agent core",
        "expected_top": "building-backend-api",
        "should_be_ambiguous": False,
    },
    {
        "prompt": "Monitor my agent's costs and errors in production",
        "description": "Observability, not deployment",
        "expected_top": "instrumenting-observability",
        "should_be_ambiguous": False,
    },
    {
        "prompt": "Which LLM should I use for my use case?",
        "description": "Research/comparison task",
        "expected_top": "researching-ai-topics",
        "should_be_ambiguous": False,
    },
    {
        "prompt": "Save the pattern we used for error handling as a reusable template",
        "description": "Pattern extraction, not skill creation",
        "expected_top": "extracting-patterns",
        "should_be_ambiguous": False,
    },
]


def test_cross_skill_routing():
    """Test 3: Cross-skill routing — ambiguous prompts resolve correctly."""
    print("\n" + "=" * 60)
    print("  TEST 3: CROSS-SKILL ROUTING")
    print("  Do ambiguous prompts route to the right skill?")
    print("=" * 60)

    skills = load_all_skills()

    for case in AMBIGUOUS_PROMPTS:
        prompt = case["prompt"]
        routing = route_prompt(prompt, skills)
        top3 = routing[:3]

        print(f"\n  \"{prompt}\"")
        print(f"  {INFO}  {case['description']}")
        if top3:
            for name, score in top3:
                print(f"         {name}: {score:.2f}")

        if case["should_be_ambiguous"]:
            if len(top3) >= 2 and top3[0][1] - top3[1][1] < 0.15:
                report("pass", "Correctly ambiguous (no dominant skill)")
            elif not top3:
                report("pass", "No strong match (ambiguous)")
            else:
                report("warn", f"Not ambiguous enough — {top3[0][0]} dominates at {top3[0][1]:.2f}")
        else:
            if top3 and top3[0][0] == case["expected_top"]:
                report("pass", f"Correct: {top3[0][0]} wins")
            elif top3:
                top_names = [r[0] for r in top3]
                if case["expected_top"] in top_names:
                    rank = top_names.index(case["expected_top"]) + 1
                    report("warn", f"Expected {case['expected_top']} but it's #{rank} (top: {top3[0][0]})")
                else:
                    report("fail", f"Expected {case['expected_top']} but got {top3[0][0]}")
            else:
                report("fail", f"Expected {case['expected_top']} but no match")


# ============================================================
# TEST SUITE 4: DESCRIPTION QUALITY (from guide's checklist)
# ============================================================

def test_description_quality():
    """Test 4: Description quality — based on guide's best practices."""
    print("\n" + "=" * 60)
    print("  TEST 4: DESCRIPTION QUALITY")
    print("  Does each description follow the guide's best practices?")
    print("=" * 60)

    skills = load_all_skills()

    for name, data in sorted(skills.items()):
        desc = data["description"]
        print(f"\n  --- {name} ---")

        # Check 1: Has trigger phrases (quoted phrases in description)
        trigger_phrases = re.findall(r'"([^"]+)"', desc)
        if len(trigger_phrases) >= 3:
            report("pass", f"Trigger phrases: {len(trigger_phrases)} defined")
        elif len(trigger_phrases) >= 1:
            report("warn", f"Trigger phrases: only {len(trigger_phrases)} (recommend 3+)")
        else:
            report("fail", f"Trigger phrases: NONE defined")

        # Check 2: Has negative triggers (Do NOT use)
        has_negative = bool(re.search(r"do not use", desc, re.IGNORECASE))
        if has_negative:
            report("pass", "Negative triggers: defined")
        else:
            report("warn", "Negative triggers: MISSING (risk of over-triggering)")

        # Check 3: Description explains WHAT the skill does (not just features)
        word_count = len(desc.split())
        if word_count >= 30:
            report("pass", f"Description length: {word_count} words (sufficient)")
        elif word_count >= 15:
            report("warn", f"Description length: {word_count} words (could be more specific)")
        else:
            report("fail", f"Description length: {word_count} words (too short)")

        # Check 4: Focuses on outcomes, not features (from guide p.20)
        # Good descriptions mention user actions ("when user says", "use when")
        has_user_context = bool(re.search(r"use when|when user", desc, re.IGNORECASE))
        if has_user_context:
            report("pass", "Outcome-focused: includes usage context")
        else:
            report("warn", "Missing usage context ('Use when...' or 'when user says...')")


# ============================================================
# TEST SUITE 5: WORKFLOW COMPLETENESS
# ============================================================

def test_workflow_completeness():
    """Test 5: Workflow completeness — does each skill have enough substance?"""
    print("\n" + "=" * 60)
    print("  TEST 5: WORKFLOW COMPLETENESS")
    print("  Does each skill have actionable content (not just routing)?")
    print("=" * 60)

    skills = load_all_skills()

    for name, data in sorted(skills.items()):
        content = data["full_content"]
        print(f"\n  --- {name} ---")

        # Count actual content lines (excluding YAML, blank lines, headers)
        lines = content.split("\n")
        content_lines = [
            l for l in lines
            if l.strip()
            and not l.strip().startswith("#")
            and not l.strip().startswith("---")
            and not l.strip().startswith("name:")
            and not l.strip().startswith("description:")
        ]

        # Check: has code examples
        has_code = bool(re.search(r"```\w*\n", content))
        if has_code:
            report("pass", "Has code examples")
        else:
            report("warn", "No code examples (skill may be too abstract)")

        # Check: has checklist or verification step
        has_checklist = bool(
            re.search(r"\[[ x]\]", content)
            or re.search(r"verify|checklist|validation", content, re.IGNORECASE)
        )
        if has_checklist:
            report("pass", "Has verification/checklist")
        else:
            report("warn", "No verification step or checklist")

        # Check: content depth (not just reference routing)
        # Count lines that are actual instructions vs "read reference" lines
        ref_routing_lines = len(re.findall(r"(?:read|load|see).*reference", content, re.IGNORECASE))
        instruction_lines = len(content_lines) - ref_routing_lines
        if instruction_lines >= 30:
            report("pass", f"Content depth: {instruction_lines} instruction lines")
        elif instruction_lines >= 15:
            report("warn", f"Content depth: {instruction_lines} instruction lines (thin)")
        else:
            report("fail", f"Content depth: {instruction_lines} instruction lines (too shallow)")


if __name__ == "__main__":
    print("=" * 60)
    print("  AGENT SKILL KIT — BEHAVIORAL TEST SUITE")
    print("  (Based on 'Complete Guide to Building Skills' Ch.3)")
    print("=" * 60)

    test_triggering()
    test_functional()
    test_cross_skill_routing()
    test_description_quality()
    test_workflow_completeness()

    print("\n" + "=" * 60)
    total = results["pass"] + results["fail"] + results["warn"]
    print(f"  RESULTS: {results['pass']} passed, {results['fail']} failed, {results['warn']} warnings  (total: {total})")
    pct = results["pass"] / total * 100 if total > 0 else 0
    print(f"  PASS RATE: {pct:.0f}%")
    print("=" * 60)

    if results["fail"] > 0:
        sys.exit(1)

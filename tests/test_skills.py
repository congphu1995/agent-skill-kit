#!/usr/bin/env python3
"""Structural validation tests for the Agent Skill Kit."""

import os
import re
import yaml
import sys
from pathlib import Path
from collections import defaultdict

SKILLS_DIR = Path(__file__).parent.parent / ".claude" / "skills"

# Expected 18 skills from blueprint
EXPECTED_SKILLS = [
    "researching-ai-topics",
    "designing-agent-system",
    "planning-and-breaking-down",
    "setting-up-ai-dev-env",
    "scaffolding-ai-project",
    "building-agent-core",
    "building-rag-pipeline",
    "building-mcp-server",
    "building-backend-api",
    "building-ai-frontend",
    "testing-ai-systems",
    "evaluating-and-benchmarking",
    "reviewing-ai-code",
    "deploying-ai-systems",
    "instrumenting-observability",
    "documenting-ai-systems",
    "creating-and-managing-skills",
    "extracting-patterns",
]

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
WARN = "\033[93mWARN\033[0m"

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


def parse_yaml_frontmatter(filepath):
    """Extract YAML frontmatter from a SKILL.md file."""
    content = filepath.read_text()
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, content
    try:
        fm = yaml.safe_load(match.group(1))
        return fm, content
    except yaml.YAMLError:
        return None, content


def extract_reference_mentions(content, skill_name):
    """Find all references/*.md mentions in a SKILL.md file.

    Filters out example references that point to OTHER skills' files,
    and example file names used in documentation prose (e.g., finance.md, mnda.md).
    """
    # Match patterns like: references/filename.md, reference/filename.md
    pattern = r"(?:references?)/([a-zA-Z0-9_-]+\.md)"
    all_mentions = re.findall(pattern, content)

    # Known example-only mentions in Anthropic-installed skills (prose examples, not real refs)
    EXAMPLE_FILES = {
        "creating-and-managing-skills": {"finance.md", "mnda.md", "policies.md", "api_docs.md", "schema.md"},
    }
    # extracting-patterns mentions other skills' references as integration examples
    CROSS_SKILL_REFS = {
        "extracting-patterns": {"langgraph-patterns.md", "state-machine-patterns.md", "llm-mocking.md"},
    }

    exclude = EXAMPLE_FILES.get(skill_name, set()) | CROSS_SKILL_REFS.get(skill_name, set())
    return [ref for ref in all_mentions if ref not in exclude]


def test_all_skills_present():
    """Test 1: All 18 expected skills have directories and SKILL.md files."""
    print("\n== Test 1: All expected skills present ==")
    for skill in EXPECTED_SKILLS:
        skill_dir = SKILLS_DIR / skill
        skill_md = skill_dir / "SKILL.md"
        if not skill_dir.exists():
            report("fail", f"Missing directory: {skill}/")
        elif not skill_md.exists():
            report("fail", f"Missing SKILL.md: {skill}/SKILL.md")
        else:
            report("pass", f"{skill}/SKILL.md exists")


def test_no_unexpected_skills():
    """Test 2: No unexpected skill directories."""
    print("\n== Test 2: No unexpected skill directories ==")
    actual_dirs = {
        d.name
        for d in SKILLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    }
    expected_set = set(EXPECTED_SKILLS)
    unexpected = actual_dirs - expected_set
    if unexpected:
        for u in unexpected:
            report("warn", f"Unexpected skill directory: {u}/")
    else:
        report("pass", "No unexpected skill directories")


def test_yaml_frontmatter():
    """Test 3: All SKILL.md files have valid YAML frontmatter with required fields."""
    print("\n== Test 3: YAML frontmatter validation ==")
    for skill in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill / "SKILL.md"
        if not skill_md.exists():
            continue
        fm, content = parse_yaml_frontmatter(skill_md)
        if fm is None:
            report("fail", f"{skill}: No valid YAML frontmatter")
            continue
        # Required fields
        # Skills installed from Anthropic keep their original names
        INSTALLED_SKILL_NAMES = {
            "building-mcp-server": "mcp-builder",
            "creating-and-managing-skills": "skill-creator",
        }
        if "name" not in fm:
            report("fail", f"{skill}: Missing 'name' in frontmatter")
        elif skill in INSTALLED_SKILL_NAMES and fm["name"] == INSTALLED_SKILL_NAMES[skill]:
            report("pass", f"{skill}: name='{fm['name']}' (installed from Anthropic, expected)")
        elif fm["name"] != skill:
            report("warn", f"{skill}: name='{fm['name']}' doesn't match directory name")
        else:
            report("pass", f"{skill}: name field correct")

        if "description" not in fm:
            report("fail", f"{skill}: Missing 'description' in frontmatter")
        elif len(str(fm["description"]).strip()) < 20:
            report("warn", f"{skill}: Description too short ({len(str(fm['description']).strip())} chars)")
        else:
            report("pass", f"{skill}: description field present")


def test_workflow_structure():
    """Test 4: All SKILL.md files have a numbered workflow or instructions section."""
    print("\n== Test 4: Workflow/Instructions structure ==")
    for skill in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text()
        # Check for numbered steps (### Step N, ### N., or numbered list)
        has_steps = bool(
            re.search(r"###\s*(Step\s+)?\d+", content)
            or re.search(r"^#{1,3}\s+\w+.*(?:Workflow|Instructions|Process|Flow)", content, re.MULTILINE)
        )
        has_numbered_list = bool(re.search(r"^\d+\.\s+\*\*", content, re.MULTILINE))
        if has_steps or has_numbered_list:
            report("pass", f"{skill}: Has structured workflow/steps")
        else:
            report("warn", f"{skill}: No clear numbered workflow found")


def test_reference_files_exist():
    """Test 5: All reference files mentioned in SKILL.md actually exist."""
    print("\n== Test 5: Reference file existence ==")
    for skill in EXPECTED_SKILLS:
        skill_dir = SKILLS_DIR / skill
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text()
        mentions = extract_reference_mentions(content, skill)
        if not mentions:
            report("pass", f"{skill}: No reference file mentions (OK)")
            continue
        for ref_file in mentions:
            # Check both references/ and reference/ directories
            ref_path_plural = skill_dir / "references" / ref_file
            ref_path_singular = skill_dir / "reference" / ref_file
            if ref_path_plural.exists() or ref_path_singular.exists():
                report("pass", f"{skill}: references/{ref_file} exists")
            else:
                report("fail", f"{skill}: references/{ref_file} NOT FOUND")


def test_directory_naming_consistency():
    """Test 6: Reference directories use consistent 'references/' naming."""
    print("\n== Test 6: Directory naming consistency ==")
    for skill in EXPECTED_SKILLS:
        skill_dir = SKILLS_DIR / skill
        if not skill_dir.exists():
            continue
        has_plural = (skill_dir / "references").exists()
        has_singular = (skill_dir / "reference").exists()
        if has_plural and has_singular:
            report("fail", f"{skill}: Has BOTH reference/ AND references/ directories")
        elif has_singular and not has_plural:
            report("warn", f"{skill}: Uses 'reference/' instead of 'references/' (inconsistent)")
        elif has_plural:
            report("pass", f"{skill}: Uses 'references/' (consistent)")
        else:
            report("pass", f"{skill}: No reference directory (OK)")


def test_reference_stubs():
    """Test 7: Identify stub reference files (< 50 lines or contains 'TODO'/'stub')."""
    print("\n== Test 7: Reference file completeness ==")
    stub_count = 0
    complete_count = 0
    for skill in EXPECTED_SKILLS:
        refs_dir = SKILLS_DIR / skill / "references"
        if not refs_dir.exists():
            refs_dir = SKILLS_DIR / skill / "reference"
        if not refs_dir.exists():
            continue
        for ref_file in sorted(refs_dir.glob("*.md")):
            content = ref_file.read_text()
            lines = len(content.splitlines())
            has_stub_marker = bool(
                re.search(r"\b(TODO|STUB|placeholder|expand after)\b", content, re.IGNORECASE)
            )
            if has_stub_marker or lines < 30:
                report("warn", f"{skill}/references/{ref_file.name}: Stub ({lines} lines)")
                stub_count += 1
            else:
                complete_count += 1
    print(f"  --- Summary: {complete_count} complete, {stub_count} stubs ---")


def test_trigger_overlaps():
    """Test 8: Check for overlapping trigger phrases between skills."""
    print("\n== Test 8: Trigger phrase overlap analysis ==")
    skill_triggers = {}
    for skill in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill / "SKILL.md"
        if not skill_md.exists():
            continue
        fm, content = parse_yaml_frontmatter(skill_md)
        if fm and "description" in fm:
            desc = str(fm["description"]).lower()
            # Extract quoted trigger phrases
            triggers = re.findall(r'"([^"]+)"', desc)
            skill_triggers[skill] = triggers

    # Check for exact duplicate triggers
    trigger_to_skills = defaultdict(list)
    for skill, triggers in skill_triggers.items():
        for t in triggers:
            trigger_to_skills[t.lower()].append(skill)

    overlaps_found = False
    for trigger, skills in sorted(trigger_to_skills.items()):
        if len(skills) > 1:
            report("warn", f"Trigger '{trigger}' shared by: {', '.join(skills)}")
            overlaps_found = True
    if not overlaps_found:
        report("pass", "No exact trigger phrase overlaps")


def test_exclusions_present():
    """Test 9: Skills with potential confusion have exclusions defined."""
    print("\n== Test 9: Exclusion clauses ==")
    # Skills that should have exclusions (related to other skills)
    should_have_exclusions = {
        "building-agent-core": ["rag", "design"],
        "building-rag-pipeline": ["agent"],
        "designing-agent-system": ["build", "implement"],
        "testing-ai-systems": ["eval"],
        "evaluating-and-benchmarking": ["unit test"],
    }
    for skill, keywords in should_have_exclusions.items():
        skill_md = SKILLS_DIR / skill / "SKILL.md"
        if not skill_md.exists():
            continue
        fm, _ = parse_yaml_frontmatter(skill_md)
        if fm and "description" in fm:
            desc = str(fm["description"]).lower()
            has_exclusion = "do not use" in desc or "not for" in desc or "exclusion" in desc
            if has_exclusion:
                report("pass", f"{skill}: Has exclusion clause")
            else:
                report("warn", f"{skill}: No exclusion clause (may confuse with related skills)")


def test_catalog_completeness():
    """Test 10: SKILL_CATALOG.md lists all 18 skills."""
    print("\n== Test 10: Catalog completeness ==")
    catalog = SKILLS_DIR / "SKILL_CATALOG.md"
    if not catalog.exists():
        report("fail", "SKILL_CATALOG.md not found")
        return
    content = catalog.read_text().lower()
    for skill in EXPECTED_SKILLS:
        if skill in content:
            report("pass", f"Catalog mentions {skill}")
        else:
            report("fail", f"Catalog missing {skill}")


def test_artifact_paths():
    """Test 11: Skills that produce artifacts define output paths."""
    print("\n== Test 11: Artifact output paths ==")
    # Skills expected to produce artifacts
    artifact_skills = [
        "designing-agent-system",
        "evaluating-and-benchmarking",
        "planning-and-breaking-down",
        "scaffolding-ai-project",
        "deploying-ai-systems",
    ]
    for skill in artifact_skills:
        skill_md = SKILLS_DIR / skill / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text()
        has_artifact_path = bool(
            re.search(r"\.claude/artifacts/", content)
            or re.search(r"artifact", content, re.IGNORECASE)
        )
        if has_artifact_path:
            report("pass", f"{skill}: Defines artifact output path")
        else:
            report("warn", f"{skill}: No artifact output path defined")


if __name__ == "__main__":
    print("=" * 60)
    print("  AGENT SKILL KIT — STRUCTURAL VALIDATION")
    print("=" * 60)

    test_all_skills_present()
    test_no_unexpected_skills()
    test_yaml_frontmatter()
    test_workflow_structure()
    test_reference_files_exist()
    test_directory_naming_consistency()
    test_reference_stubs()
    test_trigger_overlaps()
    test_exclusions_present()
    test_catalog_completeness()
    test_artifact_paths()

    print("\n" + "=" * 60)
    total = results["pass"] + results["fail"] + results["warn"]
    print(f"  RESULTS: {results['pass']} passed, {results['fail']} failed, {results['warn']} warnings  (total: {total})")
    print("=" * 60)

    if results["fail"] > 0:
        sys.exit(1)

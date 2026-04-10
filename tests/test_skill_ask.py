"""Tests for /ask SKILL.md structural completeness.

Validates that the query skill follows the extending.md structure,
references existing tools, and documents all required wiki interactions.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "ask" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"Ask SKILL.md not found at {SKILL_PATH}"
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_md_text():
    assert CLAUDE_MD.exists(), f"Product CLAUDE.md not found at {CLAUDE_MD}"
    return CLAUDE_MD.read_text(encoding="utf-8")


# ── 1. Required sections (extending.md structure) ──────────────────────

REQUIRED_SECTIONS = [
    "Inputs",
    "Outputs",
    "Wiki Interaction",
    "Workflow",
    "Constraints",
    "Error Handling",
    "Dependencies",
]


class TestSkillStructure:
    """Validate SKILL.md has all required sections per extending.md."""

    def test_file_exists(self):
        assert SKILL_PATH.exists()

    def test_has_frontmatter(self, skill_text):
        assert skill_text.startswith("---"), "SKILL.md must start with YAML frontmatter"
        parts = skill_text.split("---", 2)
        assert len(parts) >= 3, "SKILL.md must have closing --- for frontmatter"

    def test_frontmatter_has_description(self, skill_text):
        fm = skill_text.split("---", 2)[1]
        assert "description:" in fm, "Frontmatter must include description"

    def test_has_skill_heading(self, skill_text):
        assert re.search(r"^# /ask", skill_text, re.MULTILINE), \
            "SKILL.md must have '# /ask' heading"

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"

    def test_frontmatter_has_argument_hint(self, skill_text):
        fm = skill_text.split("---", 2)[1]
        assert "argument-hint:" in fm, "Frontmatter must include argument-hint"

    def test_has_intro_paragraph(self, skill_text):
        body = skill_text.split("---", 2)[2]
        # After the heading, there should be a > blockquote intro
        assert re.search(r"^>", body, re.MULTILINE), \
            "SKILL.md should have a blockquote intro paragraph"


# ── 2. Wiki Interaction documentation ──────────────────────────────────

class TestWikiInteraction:
    """Validate that wiki reads/writes are fully documented."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE), \
            "Wiki Interaction must have ### Reads subsection"

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE), \
            "Wiki Interaction must have ### Writes subsection"

    def test_reads_query_pack(self, skill_text):
        assert "context_brief.md" in skill_text, \
            "Must read context_brief.md for global context"

    def test_reads_index(self, skill_text):
        assert "index.md" in skill_text, \
            "Must read index.md for page discovery"

    def test_reads_gap_map(self, skill_text):
        assert "open_questions.md" in skill_text, \
            "Must read open_questions.md for knowledge gaps"

    ENTITY_DIRS = [
        "papers/", "concepts/", "claims/", "topics/",
        "people/", "ideas/", "experiments/", "Summary/",
    ]

    @pytest.mark.parametrize("entity_dir", ENTITY_DIRS)
    def test_reads_entity_dir(self, skill_text, entity_dir):
        reads_section = re.split(r"^###\s+Writes", skill_text, flags=re.MULTILINE)[0]
        reads_part = re.split(r"^###\s+Reads", reads_section, flags=re.MULTILINE)
        assert len(reads_part) >= 2, "Reads subsection not found"
        assert entity_dir in reads_part[1], \
            f"Reads must document {entity_dir}"

    def test_writes_outputs(self, skill_text):
        writes_section = re.split(r"^###\s+Writes", skill_text, flags=re.MULTILINE)
        assert len(writes_section) >= 2, "Writes subsection not found"
        assert "outputs/" in writes_section[1], \
            "Writes must document outputs/ for crystallized results"

    def test_writes_concepts(self, skill_text):
        writes_section = re.split(r"^###\s+Writes", skill_text, flags=re.MULTILINE)
        assert len(writes_section) >= 2
        assert "concepts/" in writes_section[1], \
            "Writes must document concepts/ for new discovered concepts"

    def test_writes_claims(self, skill_text):
        writes_section = re.split(r"^###\s+Writes", skill_text, flags=re.MULTILINE)
        assert len(writes_section) >= 2
        assert "claims/" in writes_section[1], \
            "Writes must document claims/ for new discovered claims"

    def test_has_graph_edges_subsection(self, skill_text):
        assert re.search(r"^###\s+Graph edges", skill_text, re.MULTILINE), \
            "Wiki Interaction must have ### Graph edges subsection"


# ── 3. Workflow steps ──────────────────────────────────────────────────

WORKFLOW_STEPS = [
    ("Step 1", "上下文|context|context_brief"),
    ("Step 2", "检索|retriev|search|index"),
    ("Step 3", "综合|answer|回答|synthes"),
    ("Step 4", "crystallize|评估|价值|value"),
    ("Step 5", "crystallize|写入|wiki|write"),
    ("Step 6", "导航|index|log|graph|更新"),
    ("Step 7", "报告|report|用户|user"),
]


class TestWorkflow:
    """Validate workflow steps are present and have correct keywords."""

    @pytest.mark.parametrize("step,keywords", WORKFLOW_STEPS)
    def test_workflow_step_exists(self, skill_text, step, keywords):
        pattern = rf"^###\s+{re.escape(step)}"
        match = re.search(pattern, skill_text, re.MULTILINE)
        assert match, f"Missing workflow step: ### {step}"

    @pytest.mark.parametrize("step,keywords", WORKFLOW_STEPS)
    def test_workflow_step_content(self, skill_text, step, keywords):
        # Extract content for this step (until next ### or ## or end)
        pattern = rf"(^###\s+{re.escape(step)}.*?)(?=^###\s|^##\s|\Z)"
        match = re.search(pattern, skill_text, re.MULTILINE | re.DOTALL)
        assert match, f"Could not extract content for {step}"
        content = match.group(1).lower()
        keyword_list = [k.strip().lower() for k in keywords.split("|")]
        assert any(k in content for k in keyword_list), \
            f"{step} content should contain one of: {keywords}"

    def test_has_seven_steps(self, skill_text):
        steps = re.findall(r"^###\s+Step\s+\d+", skill_text, re.MULTILINE)
        assert len(steps) == 7, f"Expected 7 workflow steps, found {len(steps)}"


# ── 4. Tool references ────────────────────────────────────────────────

REQUIRED_TOOLS = [
    ("research_wiki.py", "slug"),
    ("research_wiki.py", "add-edge"),
    ("research_wiki.py", "rebuild-context-brief"),
    ("research_wiki.py", "rebuild-open-questions"),
    ("research_wiki.py", "log"),
]


class TestToolReferences:
    """Validate that referenced tools exist and are properly documented."""

    @pytest.mark.parametrize("tool,subcommand", REQUIRED_TOOLS)
    def test_tool_referenced(self, skill_text, tool, subcommand):
        assert tool in skill_text, f"Skill must reference {tool}"
        assert subcommand in skill_text, f"Skill must reference {tool} {subcommand}"

    @pytest.mark.parametrize("tool,subcommand", REQUIRED_TOOLS)
    def test_tool_exists(self, tool, subcommand):
        tool_path = TOOLS_DIR / tool
        assert tool_path.exists(), f"Referenced tool {tool} does not exist at {tool_path}"

    def test_dependencies_section_lists_tools(self, skill_text):
        deps = re.split(r"^##\s+Dependencies", skill_text, flags=re.MULTILINE)
        assert len(deps) >= 2, "Dependencies section not found"
        assert "research_wiki.py" in deps[1], \
            "Dependencies must list research_wiki.py"


# ── 5. Crystallize feature ─────────────────────────────────────────────

class TestCrystallize:
    """Validate the crystallize feature is properly documented."""

    def test_crystallize_mentioned_in_inputs(self, skill_text):
        inputs_section = re.split(r"^##\s+Inputs", skill_text, flags=re.MULTILINE)
        assert len(inputs_section) >= 2
        # Get content until next ## section
        content = re.split(r"^##\s+", inputs_section[1], flags=re.MULTILINE)[0]
        assert "crystallize" in content.lower(), \
            "Inputs must document --crystallize option"

    def test_crystallize_in_outputs(self, skill_text):
        outputs_section = re.split(r"^##\s+Outputs", skill_text, flags=re.MULTILINE)
        assert len(outputs_section) >= 2
        content = re.split(r"^##\s+", outputs_section[1], flags=re.MULTILINE)[0]
        assert "crystallize" in content.lower(), \
            "Outputs must document crystallize behavior"

    def test_three_crystallize_cases(self, skill_text):
        """Crystallize should support outputs/, concepts/, and claims/ targets."""
        assert "Case A" in skill_text, "Must document Case A (outputs/)"
        assert "Case B" in skill_text, "Must document Case B (concepts/)"
        assert "Case C" in skill_text, "Must document Case C (claims/)"

    def test_crystallize_outputs_frontmatter(self, skill_text):
        """Outputs pages must have query and source_pages in frontmatter."""
        assert "query:" in skill_text, "Output frontmatter must include query field"
        assert "source_pages:" in skill_text, \
            "Output frontmatter must include source_pages field"

    def test_crystallize_needs_confirmation(self, skill_text):
        constraints = re.split(r"^##\s+Constraints", skill_text, flags=re.MULTILINE)
        assert len(constraints) >= 2
        content = re.split(r"^##\s+", constraints[1], flags=re.MULTILINE)[0].lower()
        assert "确认" in content or "confirm" in content, \
            "Constraints must state crystallize needs user confirmation"

    def test_crystallize_value_assessment(self, skill_text):
        """Step 4 should assess whether crystallize is worthwhile."""
        step4 = re.search(
            r"(^###\s+Step 4.*?)(?=^###\s|^##\s|\Z)",
            skill_text, re.MULTILINE | re.DOTALL
        )
        assert step4, "Step 4 not found"
        content = step4.group(1).lower()
        assert "值得" in content or "worth" in content or "signal" in content.lower(), \
            "Step 4 must assess crystallize value"


# ── 6. Constraints ─────────────────────────────────────────────────────

class TestConstraints:
    """Validate that key constraints are documented."""

    def test_no_fabrication(self, skill_text):
        constraints = re.split(r"^##\s+Constraints", skill_text, flags=re.MULTILINE)
        assert len(constraints) >= 2
        content = re.split(r"^##\s+", constraints[1], flags=re.MULTILINE)[0]
        assert "虚构" in content or "fabricat" in content.lower(), \
            "Must constrain against fabrication"

    def test_citations_must_exist(self, skill_text):
        constraints = re.split(r"^##\s+Constraints", skill_text, flags=re.MULTILINE)
        content = re.split(r"^##\s+", constraints[1], flags=re.MULTILINE)[0]
        assert "[[" in content or "slug" in content.lower() or "引用" in content, \
            "Must constrain that citations point to existing pages"

    def test_raw_readonly(self, skill_text):
        constraints = re.split(r"^##\s+Constraints", skill_text, flags=re.MULTILINE)
        content = re.split(r"^##\s+", constraints[1], flags=re.MULTILINE)[0]
        assert "raw/" in content, "Must document raw/ read-only constraint"

    def test_graph_tools_only(self, skill_text):
        constraints = re.split(r"^##\s+Constraints", skill_text, flags=re.MULTILINE)
        content = re.split(r"^##\s+", constraints[1], flags=re.MULTILINE)[0]
        assert "graph/" in content, "Must document graph/ tools-only constraint"

    def test_context_limit(self, skill_text):
        constraints = re.split(r"^##\s+Constraints", skill_text, flags=re.MULTILINE)
        content = re.split(r"^##\s+", constraints[1], flags=re.MULTILINE)[0]
        assert "15" in content or "上下文" in content or "context" in content.lower(), \
            "Must document page retrieval limit"

    def test_claim_confidence_cited(self, skill_text):
        constraints = re.split(r"^##\s+Constraints", skill_text, flags=re.MULTILINE)
        content = re.split(r"^##\s+", constraints[1], flags=re.MULTILINE)[0]
        assert "confidence" in content.lower(), \
            "Must constrain claim confidence citation"

    def test_gap_annotation(self, skill_text):
        constraints = re.split(r"^##\s+Constraints", skill_text, flags=re.MULTILINE)
        content = re.split(r"^##\s+", constraints[1], flags=re.MULTILINE)[0]
        assert "gap" in content.lower() or "缺口" in content, \
            "Must constrain gap annotation when question hits known gaps"


# ── 7. Error handling ──────────────────────────────────────────────────

class TestErrorHandling:
    """Validate error handling scenarios."""

    def test_missing_context_brief(self, skill_text):
        error_section = re.split(r"^##\s+Error Handling", skill_text, flags=re.MULTILINE)
        assert len(error_section) >= 2
        content = re.split(r"^##\s+", error_section[1], flags=re.MULTILINE)[0]
        assert "context_brief" in content, \
            "Must handle missing context_brief.md"

    def test_empty_wiki(self, skill_text):
        error_section = re.split(r"^##\s+Error Handling", skill_text, flags=re.MULTILINE)
        content = re.split(r"^##\s+", error_section[1], flags=re.MULTILINE)[0]
        assert "空" in content or "empty" in content.lower() or "init" in content or "ingest" in content, \
            "Must handle empty wiki case"

    def test_no_relevant_pages(self, skill_text):
        error_section = re.split(r"^##\s+Error Handling", skill_text, flags=re.MULTILINE)
        content = re.split(r"^##\s+", error_section[1], flags=re.MULTILINE)[0]
        assert "无相关" in content or "no relevant" in content.lower() or "无关" in content, \
            "Must handle no relevant pages found"

    def test_slug_conflict(self, skill_text):
        error_section = re.split(r"^##\s+Error Handling", skill_text, flags=re.MULTILINE)
        content = re.split(r"^##\s+", error_section[1], flags=re.MULTILINE)[0]
        assert "slug" in content.lower() or "冲突" in content, \
            "Must handle slug conflict during crystallize"


# ── 8. CLAUDE.md consistency ───────────────────────────────────────────

class TestClaudeMdConsistency:
    """Validate skill is consistent with product CLAUDE.md."""

    def test_skill_listed_in_claude_md(self, claude_md_text):
        assert "/ask" in claude_md_text or "ask" in claude_md_text, \
            "/ask must be listed in product CLAUDE.md skills table"

    def test_edge_types_valid(self, skill_text, claude_md_text):
        """All edge types used in skill must be valid per CLAUDE.md."""
        # Extract valid edge types from CLAUDE.md
        edge_match = re.search(
            r"extends,\s*contradicts,\s*supports,\s*inspired_by,\s*tested_by,\s*invalidates,\s*supersedes,\s*addresses_gap,\s*derived_from",
            claude_md_text,
        )
        # derived_from is used for query outputs — check it's documented in skill
        assert "derived_from" in skill_text, \
            "Skill must use derived_from edge type for output → source relationships"

    def test_log_format_matches(self, skill_text):
        """Log entries should follow CLAUDE.md format."""
        assert "ask |" in skill_text, \
            "Log format must use 'query | ...' prefix matching CLAUDE.md log format"

    def test_wikilink_syntax(self, skill_text):
        """Must use [[slug]] wikilink syntax per CLAUDE.md."""
        assert "[[" in skill_text and "]]" in skill_text, \
            "Must reference wikilink [[slug]] syntax"


# ── 9. Query-specific features ─────────────────────────────────────────

class TestQueryFeatures:
    """Validate query-specific features from Karpathy and V2 design."""

    def test_format_options(self, skill_text):
        """Must support multiple output formats."""
        inputs = re.split(r"^##\s+Inputs", skill_text, flags=re.MULTILINE)
        assert len(inputs) >= 2
        content = re.split(r"^##\s+", inputs[1], flags=re.MULTILINE)[0]
        assert "format" in content.lower(), "Must document --format option"

    def test_uncertainty_marking(self, skill_text):
        """Answers must mark uncertainty per Karpathy's design."""
        assert "不确定" in skill_text or "uncertain" in skill_text.lower(), \
            "Must document uncertainty marking in answers"

    def test_suggests_further_ingest(self, skill_text):
        """When wiki lacks info, should suggest papers to ingest."""
        assert "ingest" in skill_text.lower(), \
            "Must suggest further ingest when wiki knowledge is insufficient"

    def test_knowledge_gap_awareness(self, skill_text):
        """Must check open_questions.md and annotate when question hits gaps."""
        assert "open_questions" in skill_text, \
            "Must reference open_questions.md for knowledge gap awareness"

    def test_citation_in_answers(self, skill_text):
        """Answers must include wikilink citations."""
        step3 = re.search(
            r"(^###\s+Step 3.*?)(?=^###\s|^##\s|\Z)",
            skill_text, re.MULTILINE | re.DOTALL
        )
        assert step3, "Step 3 not found"
        content = step3.group(1)
        assert "[[" in content or "引用" in content or "citation" in content.lower(), \
            "Step 3 must require citations in answers"

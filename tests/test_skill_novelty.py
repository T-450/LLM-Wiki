"""Tests for /novelty SKILL.md structural completeness.

Validates that the novelty skill follows extending.md structure,
references correct tools and MCP servers, documents wiki interactions,
and aligns with product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "novelty" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"novelty SKILL.md not found at {SKILL_PATH}"
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
        assert re.search(r"^# /novelty", skill_text, re.MULTILINE), \
            "SKILL.md must have '# /novelty' heading"

    def test_has_intro_paragraph(self, skill_text):
        assert re.search(r"^>", skill_text, re.MULTILINE), \
            "SKILL.md must have intro paragraph (blockquote)"

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"


# ── 2. Wiki Interaction — READ-ONLY ───────────────────────────────────

class TestWikiInteraction:
    """Validate wiki interactions are documented and read-only."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE), \
            "Wiki Interaction must have ### Reads subsection"

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE), \
            "Wiki Interaction must have ### Writes subsection"

    def test_reads_papers(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "papers/" in reads, "Must document reading papers/"

    def test_reads_concepts(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "concepts/" in reads, "Must document reading concepts/"

    def test_reads_ideas(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "ideas/" in reads, "Must document reading ideas/"

    def test_reads_claims(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "claims/" in reads, "Must document reading claims/"

    def test_reads_query_pack(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "context_brief.md" in reads, "Must document reading context_brief.md"

    def test_writes_nothing(self, skill_text):
        """Novelty check is a pure query — must not write to wiki."""
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "无" in writes or "none" in writes.lower() or "不修改" in writes, \
            "Writes section must indicate no wiki modifications"

    def test_no_graph_edges(self, skill_text):
        """Must not create graph edges."""
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert "无" in graph or "none" in graph.lower(), \
            "Graph edges section must indicate no edges created"


# ── 3. Workflow steps ──────────────────────────────────────────────────

EXPECTED_WORKFLOW_KEYWORDS = [
    ("方法签名", "method signature"),  # Step 1: extract method signature (en) / 方法签名 (zh)
    ("搜索", "search"),                # Step 2: multi-source search (en) / 搜索 (zh)
    ("Review LLM", "review llm"),       # Step 3: Review LLM cross-verify
    ("报告", "report"),                # Step 4: generate report
]


class TestWorkflow:
    """Validate workflow covers all required steps."""

    @pytest.mark.parametrize("zh_kw,en_kw", EXPECTED_WORKFLOW_KEYWORDS)
    def test_workflow_contains_keyword(self, skill_text, zh_kw, en_kw):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert zh_kw in workflow or en_kw in workflow.lower(), \
            f"Workflow missing content containing '{zh_kw}' or '{en_kw}'"

    def test_has_at_least_4_steps(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        steps = re.findall(r"^### Step \d+", workflow, re.MULTILINE)
        assert len(steps) >= 4, f"Expected >= 4 workflow steps, found {len(steps)}"

    def test_multi_source_search(self, skill_text):
        """Step 2 must use multiple search sources."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        sources = 0
        if "WebSearch" in workflow or "Web Search" in workflow:
            sources += 1
        if "Semantic Scholar" in workflow or "fetch_s2" in workflow:
            sources += 1
        if "wiki" in workflow.lower() and ("papers/" in workflow or "concepts/" in workflow):
            sources += 1
        assert sources >= 3, f"Must use at least 3 search sources, found {sources}"

    def test_multiple_web_queries(self, skill_text):
        """Must use multiple query formulations for web search."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "5" in workflow or "多" in workflow, \
            "Should use 5+ different web search queries"


# ── 4. Novelty scoring system ──────────────────────────────────────────

class TestNoveltyScoring:
    """Validate the 1-5 novelty scoring system."""

    def test_score_range_1_to_5(self, skill_text):
        assert "1-5" in skill_text or ("1" in skill_text and "5" in skill_text), \
            "Must document 1-5 novelty scoring range"

    @pytest.mark.parametrize("score,label", [
        ("1", "Published"),
        ("2", "Very Similar"),
        ("3", "Incremental"),
        ("4", "Novel Combination"),
        ("5", "Fundamentally New"),
    ])
    def test_score_label_documented(self, skill_text, score, label):
        assert label in skill_text, \
            f"Score {score} label '{label}' must be documented"

    def test_recommendation_options(self, skill_text):
        """Must output proceed / modify / abandon recommendation."""
        for rec in ["proceed", "modify", "abandon"]:
            assert rec in skill_text, \
                f"Recommendation option '{rec}' must be documented"

    def test_conservative_scoring_principle(self, skill_text):
        """Scoring should be conservative (lower is safer)."""
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "保守" in constraints or "conservative" in constraints.lower() \
            or "低估" in constraints, \
            "Must state conservative scoring principle"


# ── 5. Review LLM cross-verification ────────────────────────────────────────

class TestLLMReviewCrossVerify:
    """Validate Review LLM integration for cross-verification."""

    def test_review_llm_in_workflow(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "review llm" in workflow.lower() or "llm-review" in workflow.lower(), \
            "Workflow must include Review LLM cross-verification step"

    def test_llm_review_mcp_reference(self, skill_text):
        assert "mcp__llm-review__chat" in skill_text, \
            "Must reference mcp__llm-review__chat tool"

    def test_review_llm_independence(self, skill_text):
        """Review LLM should assess independently, not be shown Claude's judgment."""
        assert "独立" in skill_text or "independent" in skill_text.lower(), \
            "Review LLM must assess independently"

    def test_quick_mode_skips_review_llm(self, skill_text):
        """--quick flag should skip Review LLM verification."""
        assert "quick" in skill_text.lower(), \
            "Must support --quick mode"


# ── 6. Anti-repetition (failed ideas) ─────────────────────────────────

class TestAntiRepetition:
    """Validate anti-repetition check against failed ideas."""

    def test_checks_failed_ideas(self, skill_text):
        assert "failed" in skill_text.lower() or "失败" in skill_text, \
            "Must check wiki/ideas/ for failed ideas"

    def test_failure_reason_checked(self, skill_text):
        assert "failure_reason" in skill_text, \
            "Must check failure_reason of failed ideas"

    def test_anti_repetition_in_report(self, skill_text):
        """Report must include anti-repetition findings."""
        assert "anti-repetition" in skill_text.lower() or "Anti-repetition" in skill_text, \
            "Report must include anti-repetition section"


# ── 7. Tool references ─────────────────────────────────────────────────

class TestToolReferences:
    """Validate tool references and existence."""

    def test_references_fetch_s2(self, skill_text):
        assert "fetch_s2.py" in skill_text, \
            "Must reference fetch_s2.py for Semantic Scholar queries"

    def test_fetch_s2_exists(self):
        assert (TOOLS_DIR / "fetch_s2.py").exists(), \
            "tools/fetch_s2.py must exist"

    def test_references_fetch_deepxiv_search(self, skill_text):
        assert "fetch_deepxiv.py search" in skill_text, \
            "Must reference fetch_deepxiv.py search for semantic search"

    def test_references_fetch_deepxiv_brief(self, skill_text):
        assert "fetch_deepxiv.py brief" in skill_text, \
            "Must reference fetch_deepxiv.py brief for TLDR"

    def test_fetch_deepxiv_exists(self):
        assert (TOOLS_DIR / "fetch_deepxiv.py").exists(), \
            "tools/fetch_deepxiv.py must exist"

    def test_references_web_search(self, skill_text):
        assert "WebSearch" in skill_text, \
            "Must reference WebSearch for web queries"

    def test_references_agent_tool(self, skill_text):
        """Should use Agent tool for parallel search."""
        assert "Agent" in skill_text, \
            "Should reference Agent tool for parallel search execution"


# ── 8. Constraints ─────────────────────────────────────────────────────

REQUIRED_CONSTRAINT_KEYWORDS = [
    ("不修改", "not modify"),   # no wiki writes (en: Do not modify / zh: 不修改)
    ("保守", "conservative"),   # conservative scoring (en: conservative / zh: 保守)
    ("failed", "failed"),       # must check failed ideas
    ("引用", "cite"),            # cite real sources (en: cite / zh: 引用)
]


class TestConstraints:
    """Validate constraints cover key rules."""

    @pytest.mark.parametrize("zh_kw,en_kw", REQUIRED_CONSTRAINT_KEYWORDS)
    def test_constraint_present(self, skill_text, zh_kw, en_kw):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert zh_kw in constraints or en_kw in constraints.lower(), \
            f"Constraints must mention '{zh_kw}' or '{en_kw}'"

    def test_no_wiki_modification_constraint(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("不修改 wiki" in constraints or "纯查询" in constraints or
                "not modify" in constraints.lower() or "do not modify" in constraints.lower() or
                "read-only" in constraints.lower()), \
            "Must explicitly constrain against wiki modification"


# ── 9. Error handling ──────────────────────────────────────────────────

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_websearch_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "WebSearch" in errors or "Web" in errors, \
            "Must handle WebSearch unavailability"

    def test_s2_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "Semantic Scholar" in errors or "S2" in errors, \
            "Must handle Semantic Scholar API failure"

    def test_review_llm_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "Review LLM" in errors or "review llm" in errors.lower() or "llm-review" in errors, \
            "Must handle Review LLM unavailability"

    def test_empty_wiki(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "wiki" in errors.lower() and ("空" in errors or "empty" in errors.lower()), \
            "Must handle empty wiki"

    def test_slug_not_found(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "slug" in errors.lower() or "不存在" in errors, \
            "Must handle non-existent idea slug"

    def test_deepxiv_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "deepxiv" in errors.lower() or "DeepXiv" in errors, \
            "Must handle DeepXiv API unavailability with graceful fallback"


# ── 10. CLAUDE.md consistency ──────────────────────────────────────────

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_ideas_status_referenced(self, skill_text):
        """Must reference idea status values (especially 'failed')."""
        assert "failed" in skill_text and "proposed" in skill_text, \
            "Must reference idea lifecycle statuses"

    def test_claim_status_referenced(self, skill_text):
        """Should reference claim status for context."""
        assert "claims/" in skill_text, \
            "Must reference claims for idea dependency checking"

    def test_report_structure_documented(self, skill_text):
        """Report output format must be documented."""
        assert "Score" in skill_text and "Closest Prior Work" in skill_text \
            and "Recommendation" in skill_text, \
            "Report structure must be fully documented"


# ── Helpers ─────────────────────────────────────────────────────────────

def _extract_section(text: str, heading: str, level: int = 2) -> str:
    """Extract content under a markdown heading until the next heading of same or higher level."""
    prefix = "#" * level
    pattern = rf"^{prefix}\s+{re.escape(heading)}.*?\n(.*?)(?=^{'#' * level}\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)
    # Fallback: try partial match
    pattern = rf"^{prefix}\s+.*{re.escape(heading)}.*?\n(.*?)(?=^{'#' * level}\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""

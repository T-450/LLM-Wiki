"""Tests for /survey SKILL.md structural completeness.

Validates that the survey skill follows extending.md structure,
implements 6-step workflow with thematic grouping, shared references,
and graph edge support. Aligned with product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "survey" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"survey SKILL.md not found at {SKILL_PATH}"
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_md_text():
    assert CLAUDE_MD.exists(), f"Product CLAUDE.md not found at {CLAUDE_MD}"
    return CLAUDE_MD.read_text(encoding="utf-8")


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


# ── 1. TestSkillStructure ──────────────────────────────────────────────


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
        assert "description:" in fm

    def test_has_skill_heading(self, skill_text):
        assert re.search(r"^# /survey", skill_text, re.MULTILINE)

    def test_has_intro_blockquote(self, skill_text):
        assert re.search(r"^>", skill_text, re.MULTILINE), \
            "SKILL.md must have an intro blockquote"

    def test_has_argument_hint(self, skill_text):
        fm = skill_text.split("---", 2)[1]
        assert "argument-hint:" in fm

    def test_argument_hint_has_format_flag(self, skill_text):
        fm = skill_text.split("---", 2)[1]
        assert "--format" in fm

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"


# ── 2. TestWikiInteraction ─────────────────────────────────────────────


class TestWikiInteraction:
    """Validate wiki interactions are documented."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE)

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE)

    def test_has_graph_edges_subsection(self, skill_text):
        assert re.search(r"^###\s+Graph edges", skill_text, re.MULTILINE)

    # Reads
    def test_reads_papers(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "papers/" in reads

    def test_reads_concepts(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "concepts/" in reads

    def test_reads_topics(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "topics/" in reads

    def test_reads_claims(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "claims/" in reads

    def test_reads_ideas(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "ideas/" in reads

    def test_reads_index(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "index.md" in reads

    def test_reads_query_pack(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "context_brief.md" in reads

    def test_reads_edges_jsonl(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "edges.jsonl" in reads

    def test_reads_writing_principles(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "academic-writing.md" in reads

    def test_reads_citation_discipline(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "citation-verification.md" in reads

    # Writes
    def test_writes_outputs(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "outputs/" in writes

    def test_writes_edges_jsonl(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "edges.jsonl" in writes

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    # Graph edges
    def test_graph_edge_derived_from(self, skill_text):
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert "derived_from" in graph


# ── 3. TestWorkflow ────────────────────────────────────────────────────


class TestWorkflow:
    """Validate the 6-step workflow."""

    def test_has_six_steps(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        step_matches = re.findall(r"###\s+Step\s+(\d+)", workflow)
        assert len(step_matches) >= 6, \
            f"Expected 6 steps, found {len(step_matches)}: {step_matches}"

    # Step 1: Locate knowledge
    def test_step1_parse_input(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "解析输入" in workflow or "parse" in workflow.lower()

    def test_step1_index_md(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "index.md" in workflow

    def test_step1_candidate_list(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "候选" in workflow or "candidate" in workflow.lower()

    # Step 2: Read pages
    def test_step2_read_papers(self, skill_text):
        step2 = _extract_section(skill_text, "Step 2", level=3)
        assert "Problem" in step2 or "Key idea" in step2 or "Results" in step2

    # Step 3: Thematic grouping
    def test_step3_by_research_direction(self, skill_text):
        step3 = _extract_section(skill_text, "Step 3", level=3)
        assert "研究方向" in step3 or "research direction" in step3.lower()

    def test_step3_not_per_paper(self, skill_text):
        step3 = _extract_section(skill_text, "Step 3", level=3)
        assert ("非逐篇" in step3 or "not per-paper" in step3.lower() or
                "not paper-by-paper" in step3.lower() or "not.*per.*paper" in step3.lower())

    # Step 4: Generate paragraphs
    def test_step4_topic_sentence(self, skill_text):
        step4 = _extract_section(skill_text, "Step 4", level=3)
        assert "topic sentence" in step4.lower() or "topic sentence" in step4

    def test_step4_positioning(self, skill_text):
        step4 = _extract_section(skill_text, "Step 4", level=3)
        assert "定位" in step4 or "positioning" in step4.lower() or \
               "Unlike" in step4 or "build upon" in step4.lower()

    def test_step4_de_ai_polish(self, skill_text):
        step4 = _extract_section(skill_text, "Step 4", level=3)
        assert "de-AI" in step4 or "De-AI" in step4

    # Step 5: BibTeX
    def test_step5_only_latex(self, skill_text):
        step5 = _extract_section(skill_text, "Step 5", level=3)
        assert "latex" in step5.lower() or "LaTeX" in step5

    def test_step5_dblp_crossref_s2(self, skill_text):
        step5 = _extract_section(skill_text, "Step 5", level=3)
        assert "DBLP" in step5 and "CrossRef" in step5 and "S2" in step5

    # Step 6: Archive
    def test_step6_output_file(self, skill_text):
        step6 = _extract_section(skill_text, "Step 6", level=3)
        assert "outputs/" in step6 or "related-work-" in step6

    def test_step6_graph_edges(self, skill_text):
        step6 = _extract_section(skill_text, "Step 6", level=3)
        assert "add-edge" in step6

    def test_step6_log(self, skill_text):
        step6 = _extract_section(skill_text, "Step 6", level=3)
        assert "log" in step6.lower()


# ── 4. TestToolReferences ──────────────────────────────────────────────


class TestToolReferences:
    """Validate tool references and existence."""

    def test_references_research_wiki_slug(self, skill_text):
        assert "research_wiki.py" in skill_text and "slug" in skill_text

    def test_references_research_wiki_add_edge(self, skill_text):
        assert "research_wiki.py" in skill_text and "add-edge" in skill_text

    def test_references_research_wiki_log(self, skill_text):
        assert "research_wiki.py" in skill_text and "log" in skill_text.lower()

    def test_references_fetch_s2(self, skill_text):
        assert "fetch_s2.py" in skill_text

    def test_research_wiki_exists(self):
        assert (TOOLS_DIR / "research_wiki.py").exists()

    def test_fetch_s2_exists(self):
        assert (TOOLS_DIR / "fetch_s2.py").exists()

    def test_references_webfetch_for_bibtex(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "WebFetch" in deps or "DBLP" in deps or "CrossRef" in deps


# ── 5. TestOutputFormats ───────────────────────────────────────────────


class TestOutputFormats:
    """Validate support for latex and markdown output formats."""

    def test_supports_latex_format(self, skill_text):
        assert "latex" in skill_text.lower()

    def test_supports_markdown_format(self, skill_text):
        assert "markdown" in skill_text.lower()

    def test_latex_uses_cite(self, skill_text):
        assert r"\cite{" in skill_text or r"\cite" in skill_text

    def test_markdown_uses_wikilinks(self, skill_text):
        assert "[[slug]]" in skill_text

    def test_default_is_latex(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "默认" in inputs and "latex" in inputs.lower() or \
               "default" in inputs.lower() and "latex" in inputs.lower()


# ── 6. TestGroupingRules ───────────────────────────────────────────────


class TestGroupingRules:
    """Validate thematic grouping rules."""

    def test_group_by_research_direction(self, skill_text):
        step3 = _extract_section(skill_text, "Step 3", level=3)
        assert "研究方向分组" in step3 or "group" in step3.lower()

    def test_not_per_paper_listing(self, skill_text):
        step3 = _extract_section(skill_text, "Step 3", level=3)
        assert ("非逐篇" in step3 or "not per-paper" in step3.lower() or
                "非单篇" in step3 or "not paper-by-paper" in step3.lower())

    def test_each_group_has_positioning(self, skill_text):
        step3 = _extract_section(skill_text, "Step 3", level=3)
        assert "与本文" in step3 or "Unlike" in step3 or \
               "our method" in step3.lower() or "build upon" in step3.lower()

    def test_group_order_documented(self, skill_text):
        step3 = _extract_section(skill_text, "Step 3", level=3)
        assert "顺序" in step3 or "order" in step3.lower()

    def test_papers_per_group_range(self, skill_text):
        step3 = _extract_section(skill_text, "Step 3", level=3)
        assert "3-8" in step3 or ("3" in step3 and "8" in step3)

    def test_important_papers_more_detail(self, skill_text):
        step3 = _extract_section(skill_text, "Step 3", level=3)
        assert "重要" in step3 or "详写" in step3 or "important" in step3.lower()


# ── 7. TestDeAiPolish ──────────────────────────────────────────────────


class TestDeAiPolish:
    """Validate de-AI polish requirements."""

    def test_mentions_de_ai_polish(self, skill_text):
        assert "de-AI" in skill_text or "De-AI" in skill_text

    def test_references_writing_principles(self, skill_text):
        assert "academic-writing.md" in skill_text

    def test_polish_is_mandatory(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "de-AI" in constraints or "polish" in constraints.lower() or \
               "必选" in constraints


# ── 8. TestCitationHandling ────────────────────────────────────────────


class TestCitationHandling:
    """Validate citation handling rules."""

    def test_references_citation_discipline(self, skill_text):
        assert "citation-verification.md" in skill_text

    def test_only_cite_wiki_papers(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "wiki" in constraints.lower() and \
               ("已有" in constraints or "只引用" in constraints or "only" in constraints.lower())

    def test_verify_placeholder(self, skill_text):
        assert "[UNCONFIRMED]" in skill_text

    def test_mentions_dblp(self, skill_text):
        assert "DBLP" in skill_text

    def test_mentions_crossref(self, skill_text):
        assert "CrossRef" in skill_text

    def test_mentions_s2(self, skill_text):
        assert "S2" in skill_text


# ── 9. TestConstraints ─────────────────────────────────────────────────


class TestConstraints:
    """Validate constraints cover key rules."""

    def test_only_cite_wiki_papers(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "只引用" in constraints or "wiki" in constraints.lower()

    def test_group_by_theme_not_per_paper(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("主题分组" in constraints or "按主题" in constraints or
                "非逐篇" in constraints or "group by theme" in constraints.lower() or
                "not as a flat list" in constraints.lower())

    def test_each_group_has_positioning(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "定位" in constraints or "positioning" in constraints.lower() or \
               "定位句" in constraints

    def test_warn_if_less_than_5_papers(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "5" in constraints and ("警告" in constraints or "warn" in constraints.lower() or "< 5" in constraints)

    def test_bibtex_follows_citation_discipline(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "citation-verification" in constraints or "BibTeX" in constraints

    def test_de_ai_polish_mandatory(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "de-AI" in constraints or "polish" in constraints.lower() or \
               "必选" in constraints

    def test_archive_to_outputs(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "outputs/" in constraints or "归档" in constraints

    def test_graph_edges_via_tool(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "research_wiki.py" in constraints or "tools/" in constraints or \
               "不手动" in constraints


# ── 10. TestErrorHandling ──────────────────────────────────────────────


class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_wiki_papers_less_than_3(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "3" in errors and (
            "不足" in errors or "论文" in errors or
            "paper" in errors.lower() or "fewer" in errors.lower()
        )

    def test_no_matching_papers(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "无匹配" in errors or "no match" in errors.lower() or \
               "扩大搜索" in errors

    def test_bibtex_fetch_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "BibTeX" in errors and ("[UNCONFIRMED]" in errors or "失败" in errors)

    def test_slug_conflict(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "slug" in errors.lower() and ("冲突" in errors or "conflict" in errors.lower())


# ── 11. TestSharedReferences ───────────────────────────────────────────


class TestSharedReferences:
    """Validate shared references are used and exist."""

    def test_writing_principles_referenced(self, skill_text):
        assert "academic-writing.md" in skill_text

    def test_writing_principles_exists(self):
        assert (SHARED_REFS / "academic-writing.md").exists(), \
            f"academic-writing.md not found at {SHARED_REFS}"

    def test_citation_discipline_referenced(self, skill_text):
        assert "citation-verification.md" in skill_text

    def test_citation_discipline_exists(self):
        assert (SHARED_REFS / "citation-verification.md").exists(), \
            f"citation-verification.md not found at {SHARED_REFS}"


# ── 12. TestClaudeMdConsistency ────────────────────────────────────────


class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_skill_in_claude_md(self, claude_md_text):
        assert "/survey" in claude_md_text, \
            "/survey must be listed in product CLAUDE.md"

    def test_log_format_matches(self, skill_text):
        """Log entry should use 'survey |' pipe-separated format."""
        assert "survey |" in skill_text or \
               "survey |" in skill_text.replace("\\n", "\n")

    def test_edge_type_derived_from_valid(self, claude_md_text):
        assert "derived_from" in claude_md_text, \
            "derived_from must be a valid edge type in product CLAUDE.md"

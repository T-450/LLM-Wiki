"""Tests for /paper-draft SKILL.md structural completeness.

Validates that the paper-draft skill follows extending.md structure,
implements section-by-section LaTeX drafting from wiki, de-AI polish,
citation handling, figure generation, and aligns with product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "paper-draft" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"
TOOLS_DIR = PROJECT_ROOT / "tools"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"paper-draft SKILL.md not found at {SKILL_PATH}"
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_md_text():
    assert CLAUDE_MD.exists(), f"Product CLAUDE.md not found at {CLAUDE_MD}"
    return CLAUDE_MD.read_text(encoding="utf-8")


# ── Helpers ─────────────────────────────────────────────────────────────

def _extract_section(text: str, heading: str, level: int = 2) -> str:
    """Extract content under a markdown heading until next heading of same or higher level."""
    prefix = "#" * level
    pattern = rf"^{prefix}\s+{re.escape(heading)}.*?\n(.*?)(?=^{'#' * level}\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)
    # Fallback: partial match
    pattern = rf"^{prefix}\s+.*{re.escape(heading)}.*?\n(.*?)(?=^{'#' * level}\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


# ── 1. TestSkillStructure (~9 tests) ───────────────────────────────────

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
        assert re.search(r"^# /paper-draft", skill_text, re.MULTILINE)

    def test_has_intro_blockquote(self, skill_text):
        assert re.search(r"^>", skill_text, re.MULTILINE)

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"


# ── 2. TestWikiInteraction (~16 tests) ──────────────────────────────────

class TestWikiInteraction:
    """Validate wiki read/write/graph interactions."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE)

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE)

    def test_has_graph_edges_subsection(self, skill_text):
        assert re.search(r"^###\s+Graph", skill_text, re.MULTILINE)

    def test_reads_claims(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "claims/" in reads

    def test_reads_experiments(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "experiments/" in reads

    def test_reads_papers(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "papers/" in reads

    def test_reads_concepts(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "concepts/" in reads

    def test_reads_topics(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "topics/" in reads

    def test_reads_ideas(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "ideas/" in reads

    def test_reads_people(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "people/" in reads

    def test_reads_edges_jsonl(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "edges.jsonl" in reads

    def test_reads_gap_map(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "open_questions.md" in reads

    def test_reads_writing_principles(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "academic-writing.md" in reads

    def test_reads_citation_discipline(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "citation-verification.md" in reads

    def test_writes_paper_directory(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "paper/" in writes

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    def test_graph_edges_none(self, skill_text):
        """paper-plan already created graph edges, so paper-write should create none."""
        graph = _extract_section(skill_text, "Graph", level=3)
        assert "无" in graph or "none" in graph.lower() or "paper-plan" in graph.lower()


# ── 3. TestWorkflow (~12 tests) ─────────────────────────────────────────

class TestWorkflow:
    """Validate the 6-step workflow."""

    def test_has_six_steps(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        for i in range(1, 7):
            assert f"Step {i}" in workflow, f"Missing Step {i} in workflow"

    def test_step1_init_paper_dir(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "paper/" in workflow

    def test_step1_venue_template(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "template" in workflow.lower()

    def test_step1_math_commands(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "math_commands.tex" in workflow

    def test_step1_main_tex(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "main.tex" in workflow

    def test_step2_matplotlib(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "matplotlib" in workflow

    def test_step2_colorblind_safe(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert re.search(r"[Cc]olorblind", workflow)

    def test_step2_pdf_format(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "PDF" in workflow or ".pdf" in workflow

    def test_step3_per_section_from_wiki(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "wiki" in workflow.lower() and "section" in workflow.lower()

    def test_step3_de_ai_polish(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert re.search(r"[Dd]e-AI", workflow) or "de-AI" in workflow

    def test_step3_claim_first_experiments(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "claim-first" in workflow.lower() or "claim" in workflow.lower()

    def test_step4_dblp_crossref(self, skill_text):
        """DBLP/CrossRef may be in workflow or constraints/dependencies; at minimum BibTeX in Step 4."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "BibTeX" in workflow or "references.bib" in workflow
        # DBLP/CrossRef must be mentioned somewhere in the skill
        assert "DBLP" in skill_text and "CrossRef" in skill_text

    def test_step4_verify_protocol(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "[UNCONFIRMED]" in workflow

    def test_step5_llm_review_cross_review(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "mcp__llm-review__chat" in workflow

    def test_step6_output(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Step 6" in workflow


# ── 4. TestToolReferences (~7 tests) ────────────────────────────────────

class TestToolReferences:
    """Validate tool references in Dependencies."""

    def test_references_research_wiki_log(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "research_wiki.py" in deps and "log" in deps

    def test_references_fetch_s2(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "fetch_s2.py" in deps

    def test_references_python3_matplotlib(self, skill_text):
        assert "python3" in skill_text and "matplotlib" in skill_text

    def test_references_webfetch_dblp(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "WebFetch" in deps or "DBLP" in deps

    def test_references_webfetch_crossref(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "WebFetch" in deps or "CrossRef" in deps

    def test_research_wiki_exists(self):
        assert (TOOLS_DIR / "research_wiki.py").exists()

    def test_fetch_s2_exists(self):
        assert (TOOLS_DIR / "fetch_s2.py").exists()


# ── 5. TestLatexOutput (~10 tests) ──────────────────────────────────────

class TestLatexOutput:
    """Validate LaTeX output structure references."""

    def test_mentions_main_tex(self, skill_text):
        assert "main.tex" in skill_text

    def test_mentions_sections_directory(self, skill_text):
        assert "sections/" in skill_text

    def test_mentions_math_commands(self, skill_text):
        assert "math_commands.tex" in skill_text

    def test_mentions_references_bib(self, skill_text):
        assert "references.bib" in skill_text

    def test_mentions_figures_directory(self, skill_text):
        assert "figures/" in skill_text

    def test_lists_introduction_tex(self, skill_text):
        assert "introduction.tex" in skill_text

    def test_lists_related_work_tex(self, skill_text):
        assert "related_work.tex" in skill_text

    def test_lists_method_tex(self, skill_text):
        assert "method.tex" in skill_text

    def test_lists_experiments_tex(self, skill_text):
        assert "experiments.tex" in skill_text

    def test_lists_conclusion_tex(self, skill_text):
        assert "conclusion.tex" in skill_text

    def test_mentions_booktabs(self, skill_text):
        assert "booktabs" in skill_text

    def test_mentions_cite_command(self, skill_text):
        assert r"\cite{" in skill_text or r"\cite{key}" in skill_text

    def test_mentions_ref_command(self, skill_text):
        assert r"\ref{" in skill_text

    def test_mentions_venue_template(self, skill_text):
        assert "venue" in skill_text.lower() and "template" in skill_text.lower()


# ── 6. TestDeAiPolish (~6 tests) ────────────────────────────────────────

class TestDeAiPolish:
    """Validate de-AI polish requirements."""

    def test_mentions_de_ai_polish(self, skill_text):
        assert re.search(r"[Dd]e-AI\s+[Pp]olish", skill_text)

    def test_references_writing_principles_for_polish(self, skill_text):
        assert "academic-writing.md" in skill_text

    def test_mentions_ai_characteristic_words(self, skill_text):
        """Should list AI-characteristic words to avoid."""
        lower = skill_text.lower()
        ai_words_found = sum(1 for w in ["delve", "leverage", "utilize", "comprehensive"]
                             if w in lower)
        assert ai_words_found >= 2, "Should mention at least 2 AI-characteristic words"

    def test_mentions_active_voice(self, skill_text):
        assert "active voice" in skill_text.lower()

    def test_mentions_notation_consistency(self, skill_text):
        assert "notation" in skill_text.lower() and "consisten" in skill_text.lower()

    def test_polish_mandatory(self, skill_text):
        """De-AI polish must not be optional."""
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("必选" in constraints or "必须" in constraints or
                "mandatory" in constraints.lower() or "不可跳过" in constraints)


# ── 7. TestCitationHandling (~6 tests) ──────────────────────────────────

class TestCitationHandling:
    """Validate citation handling follows citation-verification.md."""

    def test_references_citation_discipline(self, skill_text):
        assert "citation-verification.md" in skill_text

    def test_mentions_dblp(self, skill_text):
        assert "DBLP" in skill_text

    def test_mentions_crossref(self, skill_text):
        assert "CrossRef" in skill_text

    def test_mentions_verify_protocol(self, skill_text):
        assert "[UNCONFIRMED]" in skill_text

    def test_nocite_prohibited(self, skill_text):
        assert r"\nocite" in skill_text or "nocite" in skill_text

    def test_wikilink_to_cite_conversion(self, skill_text):
        assert "[[" in skill_text and r"\cite" in skill_text


# ── 8. TestFigureGeneration (~5 tests) ──────────────────────────────────

class TestFigureGeneration:
    """Validate figure generation requirements."""

    def test_mentions_matplotlib(self, skill_text):
        assert "matplotlib" in skill_text

    def test_mentions_colorblind_safe(self, skill_text):
        assert re.search(r"[Cc]olorblind", skill_text)

    def test_mentions_font_size(self, skill_text):
        assert "font size" in skill_text.lower() or "8pt" in skill_text

    def test_mentions_pdf_format(self, skill_text):
        assert ".pdf" in skill_text or "PDF" in skill_text

    def test_figure_plan_from_paper_plan(self, skill_text):
        assert "PAPER_PLAN" in skill_text and ("Figure Plan" in skill_text or "figure" in skill_text.lower())


# ── 9. TestConstraints (~8 tests) ───────────────────────────────────────

class TestConstraints:
    """Validate key constraints are documented."""

    def test_every_section_from_wiki(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "wiki" in constraints.lower() and ("取材" in constraints or "from wiki" in constraints.lower())

    def test_bibtex_from_citation_discipline(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "citation-verification" in constraints

    def test_de_ai_polish_mandatory(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "polish" in constraints.lower() or "polish" in constraints

    def test_figures_follow_writing_principles(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "academic-writing" in constraints or "colorblind" in constraints.lower() or "figure" in constraints.lower()

    def test_anonymous_submission(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "匿名" in constraints or "anonymous" in constraints.lower()

    def test_nocite_forbidden(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "nocite" in constraints.lower()

    def test_notation_consistency_math_commands(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "math_commands" in constraints or "notation" in constraints.lower()

    def test_backup_before_overwrite(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("备份" in constraints or "backup" in constraints.lower() or
                "覆盖" in constraints or "back up" in constraints.lower() or
                "overwrite" in constraints.lower())


# ── 10. TestErrorHandling (~5 tests) ────────────────────────────────────

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_paper_plan_not_found(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "PAPER_PLAN" in errors and ("找不到" in errors or "not found" in errors.lower())

    def test_wiki_page_missing(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("wiki" in errors.lower() and
                ("找不到" in errors or "不存在" in errors or "missing" in errors.lower()))

    def test_figure_generation_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("figure" in errors.lower() or "matplotlib" in errors) and \
               ("失败" in errors or "fail" in errors.lower() or "TODO" in errors)

    def test_bibtex_fetch_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "BibTeX" in errors and ("失败" in errors or "fail" in errors.lower())

    def test_review_llm_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("Review LLM" in errors or "review llm" in errors.lower() or "llm-review" in errors) and ("不可用" in errors or "unavail" in errors.lower() or "跳过" in errors)


# ── 11. TestSharedReferences (~3 tests) ─────────────────────────────────

class TestSharedReferences:
    """Validate shared references are referenced and exist."""

    def test_writing_principles_referenced(self, skill_text):
        assert "academic-writing.md" in skill_text

    def test_writing_principles_exists(self):
        assert (SHARED_REFS / "academic-writing.md").exists()

    def test_citation_discipline_referenced(self, skill_text):
        assert "citation-verification.md" in skill_text

    def test_citation_discipline_exists(self):
        assert (SHARED_REFS / "citation-verification.md").exists()


# ── 12. TestClaudeMdConsistency (~3 tests) ──────────────────────────────

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_paper_write_in_claude_md(self, claude_md_text):
        assert "/paper-draft" in claude_md_text or "paper-write" in claude_md_text, \
            "paper-draft skill should be registered in product CLAUDE.md"

    def test_log_format_matches(self, skill_text):
        """Skill should use research_wiki.py log for consistent log format."""
        assert "research_wiki.py" in skill_text and "log" in skill_text

    def test_uses_wikilink_syntax(self, skill_text):
        assert "[[" in skill_text

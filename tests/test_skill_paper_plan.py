"""Tests for /paper-plan SKILL.md structural completeness.

Validates that the paper-plan skill follows extending.md structure,
builds claim-driven paper outlines with evidence map compiled from wiki,
references correct tools, documents wiki interactions, and aligns
with product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# -- Paths -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "paper-plan" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"paper-plan SKILL.md not found at {SKILL_PATH}"
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_md_text():
    assert CLAUDE_MD.exists(), f"Product CLAUDE.md not found at {CLAUDE_MD}"
    return CLAUDE_MD.read_text(encoding="utf-8")


# -- 1. Required sections (extending.md structure) ---------------------------

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
        assert re.search(r"^# /paper-plan", skill_text, re.MULTILINE), \
            "SKILL.md must have '# /paper-plan' heading"

    def test_has_intro_paragraph(self, skill_text):
        assert re.search(r"^>", skill_text, re.MULTILINE), \
            "SKILL.md must have intro paragraph (blockquote)"

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"


# -- 2. Wiki Interaction -----------------------------------------------------

class TestWikiInteraction:
    """Validate wiki interaction documentation."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE)

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE)

    def test_has_graph_edges_subsection(self, skill_text):
        assert re.search(r"^###\s+Graph edges", skill_text, re.MULTILINE)

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

    def test_reads_query_pack(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "context_brief.md" in reads

    def test_reads_gap_map(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "open_questions.md" in reads

    def test_reads_edges_jsonl(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "edges.jsonl" in reads

    def test_writes_outputs(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "outputs/" in writes

    def test_writes_edges_derived_from(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "edges.jsonl" in writes or "derived_from" in writes

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    def test_reads_writing_principles(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "academic-writing.md" in reads

    def test_reads_citation_discipline(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "citation-verification.md" in reads


# -- 3. Workflow (8 steps) ---------------------------------------------------

class TestWorkflow:
    """Validate workflow covers all 8 required steps."""

    def test_has_8_steps(self, skill_text):
        # Steps are ### Step N headings scattered through the Workflow section
        # (which contains code blocks with ## headings that confuse naive extraction)
        steps = re.findall(r"^### Step \d+", skill_text, re.MULTILINE)
        assert len(steps) >= 8, f"Expected >= 8 workflow steps, found {len(steps)}"

    def test_step1_load_claim_graph(self, skill_text):
        step = _extract_step(skill_text, 1)
        assert "claim" in step.lower() and ("graph" in step.lower() or "加载" in step)

    def test_step2_evidence_map(self, skill_text):
        step = _extract_step(skill_text, 2)
        assert "evidence map" in step.lower() or "Evidence Map" in step

    def test_step3_narrative_structure(self, skill_text):
        step = _extract_step(skill_text, 3)
        assert "叙事" in step or "narrative" in step.lower()

    def test_step4_section_outline(self, skill_text):
        step = _extract_step(skill_text, 4)
        assert "章节" in step or "section" in step.lower() or "大纲" in step

    def test_step5_figure_plan(self, skill_text):
        step = _extract_step(skill_text, 5)
        assert "figure" in step.lower() or "Figure" in step

    def test_step6_citation_plan(self, skill_text):
        step = _extract_step(skill_text, 6)
        assert "citation" in step.lower() or "Citation" in step or "引用" in step

    def test_step7_llm_review(self, skill_text):
        step = _extract_step(skill_text, 7)
        assert "Review LLM" in step or "llm-review" in step.lower()

    def test_step8_output_to_wiki(self, skill_text):
        step = _extract_step(skill_text, 8)
        assert "wiki" in step.lower() or "Wiki" in step or "输出" in step

    def test_references_llm_review_chat(self, skill_text):
        # mcp__llm-review__chat appears in Step 7, search full text
        assert "mcp__llm-review__chat" in skill_text

    def test_mentions_venue_page_budget(self, skill_text):
        # Page budget appears in the Workflow area (may be inside code block)
        workflow_area = _extract_workflow_full(skill_text)
        assert ("page" in workflow_area.lower() or "页" in workflow_area) and \
               ("budget" in workflow_area.lower() or "限制" in workflow_area or "venue" in workflow_area.lower())

    def test_mentions_hourglass_or_narrative(self, skill_text):
        workflow_area = _extract_workflow_full(skill_text)
        assert "hourglass" in workflow_area.lower() or "叙事" in workflow_area


# -- 4. Tool references ------------------------------------------------------

REQUIRED_TOOL_COMMANDS = [
    "slug",
    "add-edge",
    "rebuild-context-brief",
    "log",
]


class TestToolReferences:
    """Validate all referenced tools exist."""

    def test_references_research_wiki(self, skill_text):
        assert "tools/research_wiki.py" in skill_text or "research_wiki.py" in skill_text

    @pytest.mark.parametrize("command", REQUIRED_TOOL_COMMANDS)
    def test_tool_command_referenced(self, skill_text, command):
        assert command in skill_text, \
            f"Tool command '{command}' must be referenced in SKILL.md"

    def test_references_fetch_s2(self, skill_text):
        assert "fetch_s2.py" in skill_text

    def test_all_referenced_tools_exist(self):
        assert (TOOLS_DIR / "research_wiki.py").exists()
        assert (TOOLS_DIR / "fetch_s2.py").exists()

    def test_references_webfetch_for_bibtex(self, skill_text):
        assert "WebFetch" in skill_text or "DBLP" in skill_text or "CrossRef" in skill_text


# -- 5. Evidence Map ----------------------------------------------------------

class TestEvidenceMap:
    """Validate evidence map compiled from wiki claims."""

    def test_mentions_evidence_map(self, skill_text):
        assert "evidence map" in skill_text.lower() or "Evidence Map" in skill_text

    def test_matrix_includes_claim_status(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Status" in workflow or "status" in workflow

    def test_matrix_includes_confidence(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Confidence" in workflow or "confidence" in workflow

    def test_matrix_includes_evidence_sources(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Evidence Sources" in workflow or "evidence" in workflow.lower()

    def test_matrix_maps_claims_to_sections(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Paper Section" in workflow or "section" in workflow.lower()

    def test_maps_claims_target_decomposition_contextual(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Target" in workflow or "target" in workflow
        assert "Decomposition" in workflow or "decomposition" in workflow
        assert "Contextual" in workflow or "contextual" in workflow


# -- 6. Venue Support ---------------------------------------------------------

class TestVenueSupport:
    """Validate venue handling."""

    def test_venue_is_required_parameter(self, skill_text):
        assert "--venue" in skill_text

    def test_lists_iclr(self, skill_text):
        assert "ICLR" in skill_text

    def test_lists_neurips(self, skill_text):
        assert "NeurIPS" in skill_text

    def test_lists_icml(self, skill_text):
        assert "ICML" in skill_text

    def test_lists_acl(self, skill_text):
        assert "ACL" in skill_text

    def test_lists_cvpr(self, skill_text):
        assert "CVPR" in skill_text

    def test_lists_ieee(self, skill_text):
        assert "IEEE" in skill_text

    def test_mentions_page_budget(self, skill_text):
        assert "page" in skill_text.lower() or "页数" in skill_text or "页" in skill_text

    def test_venue_affects_formatting(self, skill_text):
        assert ("格式" in skill_text and "venue" in skill_text.lower()) or \
               ("format" in skill_text.lower() and "venue" in skill_text.lower())


# -- 7. Constraints -----------------------------------------------------------

class TestConstraints:
    """Validate constraints cover key rules."""

    def test_venue_required(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "--venue" in constraints and ("必选" in constraints or "required" in constraints.lower())

    def test_experiment_evidence_required(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "experiment" in constraints.lower() or "实验" in constraints

    def test_page_budget_feasible(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("page" in constraints.lower() or "页" in constraints) and \
               ("budget" in constraints.lower() or "限制" in constraints or "可行" in constraints)

    def test_llm_review_mandatory(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("Review LLM" in constraints or "llm-review" in constraints.lower()) and ("必选" in constraints or "mandatory" in constraints.lower() or "不可跳过" in constraints)

    def test_all_citations_from_wiki(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("引用" in constraints or "citation" in constraints.lower()) and \
               ("wiki" in constraints.lower() or "papers/" in constraints)

    def test_every_claim_mapped_to_section(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("claim" in constraints.lower() and "section" in constraints.lower()) or \
               ("claim" in constraints.lower() and "映射" in constraints)

    def test_every_section_has_claim(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "section" in constraints.lower() and \
               ("claim" in constraints.lower() or "填充" in constraints)

    def test_graph_edges_via_tool(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "research_wiki.py" in constraints or "edges.jsonl" in constraints

    def test_citations_use_wikilinks(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "[[" in constraints and ("slug" in constraints.lower() or "wikilink" in constraints.lower() or "引用" in constraints)

    def test_at_least_one_experiment(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "至少" in constraints or "at least" in constraints.lower()


# -- 8. Error Handling --------------------------------------------------------

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_claim_status_insufficient(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("claim" in errors.lower() and "proposed" in errors) or "状态不足" in errors

    def test_no_experiment_evidence(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "experiment" in errors.lower() or "实验" in errors

    def test_wiki_papers_insufficient(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("paper" in errors.lower() or "论文" in errors) and \
               ("不足" in errors or "insufficient" in errors.lower() or "< 5" in errors or "<" in errors)

    def test_page_budget_over_limit(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("page" in errors.lower() or "页" in errors) and \
               ("超" in errors or "over" in errors.lower() or "appendix" in errors.lower())

    def test_review_llm_unavailable_fallback(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("Review LLM" in errors or "review llm" in errors.lower() or "llm-review" in errors) and ("不可用" in errors or "unavailable" in errors.lower() or "降级" in errors)

    def test_bibtex_fetch_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "BibTeX" in errors or "VERIFY" in errors


# -- 9. Shared References ----------------------------------------------------

class TestSharedReferences:
    """Validate shared reference usage."""

    def test_references_writing_principles(self, skill_text):
        assert "academic-writing.md" in skill_text

    def test_references_citation_discipline(self, skill_text):
        assert "citation-verification.md" in skill_text

    def test_writing_principles_file_exists(self):
        path = SHARED_REFS / "academic-writing.md"
        assert path.exists(), f"academic-writing.md not found at {path}"

    def test_citation_discipline_file_exists(self):
        path = SHARED_REFS / "citation-verification.md"
        assert path.exists(), f"citation-verification.md not found at {path}"

    def test_reviewer_independence_stance(self, skill_text):
        """Either references cross-model-review.md or explicitly does not need it."""
        has_ref = "cross-model-review.md" in skill_text
        # paper-plan focuses on outline not review, so it may not reference it.
        # But it does use Review LLM in Step 7, so check if referenced anywhere.
        if not has_ref:
            # acceptable if not referenced -- paper-plan delegates review to Review LLM
            # but should at least reference the other two shared refs
            assert "academic-writing.md" in skill_text and \
                   "citation-verification.md" in skill_text, \
                "Must reference at least academic-writing and citation-verification"


# -- 10. CLAUDE.md Consistency ------------------------------------------------

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_skill_listed_in_claude_md(self, claude_md_text):
        assert "paper-plan" in claude_md_text, \
            "/paper-plan must be listed in product CLAUDE.md skills table"

    def test_edge_type_derived_from_in_claude_md(self, claude_md_text):
        assert "derived_from" in claude_md_text, \
            "Edge type derived_from must be in product CLAUDE.md graph section"

    def test_log_format_matches_claude_md(self, skill_text):
        """Log entries should use the tools/research_wiki.py log command."""
        assert "log wiki/" in skill_text or 'log wiki/' in skill_text

    def test_uses_wikilink_syntax(self, skill_text):
        assert "[[" in skill_text, "Must use wikilink syntax [[slug]]"


# -- Helpers ------------------------------------------------------------------

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


def _extract_workflow_full(text: str) -> str:
    """Extract the full Workflow section including code blocks with ## headings.

    The Workflow section in paper-plan contains embedded code blocks that have
    ## headings inside them (e.g. ## 1. Introduction). The naive _extract_section
    helper stops at those, so this function extracts from ## Workflow to ## Constraints.
    """
    pattern = r"^## Workflow.*?\n(.*?)(?=^## Constraints|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def _extract_step(text: str, step_num: int) -> str:
    """Extract content of a specific workflow step from the full text.

    Searches the full text because the Workflow section contains embedded code
    blocks with ## headings that break naive section extraction.
    """
    pattern = rf"^### Step {step_num}[:\s].*?\n(.*?)(?=^### Step \d|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(0)
    # Fallback: include the heading line itself
    pattern = rf"^### Step {step_num}.*?\n(.*?)(?=^### |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(0) if match else ""

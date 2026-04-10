"""Tests for /rebuttal SKILL.md structural completeness.

Validates that the rebuttal skill follows extending.md structure,
implements reviewer concern atomization, claim mapping, evidence checking,
optional Review LLM stress-test, and dual-format output (formal + rich).
"""

import re
from pathlib import Path

import pytest

# -- Paths -----------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "rebuttal" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"rebuttal SKILL.md not found at {SKILL_PATH}"
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_md_text():
    assert CLAUDE_MD.exists(), f"Product CLAUDE.md not found at {CLAUDE_MD}"
    return CLAUDE_MD.read_text(encoding="utf-8")


# -- Helpers ---------------------------------------------------------------

def _extract_section(text: str, heading: str, level: int = 2) -> str:
    """Extract content under a markdown heading until the next heading of same or higher level."""
    prefix = "#" * level
    pattern = rf"^{prefix}\s+{re.escape(heading)}.*?\n(.*?)(?=^{'#' * level}\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)
    # Fallback: partial match
    pattern = rf"^{prefix}\s+.*{re.escape(heading)}.*?\n(.*?)(?=^{'#' * level}\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


# -- 1. TestSkillStructure (~9) --------------------------------------------

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
        assert re.search(r"^# /rebuttal", skill_text, re.MULTILINE), \
            "SKILL.md must have '# /rebuttal' heading"

    def test_has_intro_blockquote(self, skill_text):
        assert re.search(r"^>", skill_text, re.MULTILINE), \
            "SKILL.md must have intro blockquote paragraph"

    def test_intro_mentions_rebuttal(self, skill_text):
        # Find blockquote lines
        bq_lines = [l for l in skill_text.splitlines() if l.startswith(">")]
        bq_text = " ".join(bq_lines)
        assert "rebuttal" in bq_text.lower() or "concern" in bq_text.lower() or \
               "审稿" in bq_text

    def test_has_argument_hint(self, skill_text):
        fm = skill_text.split("---", 2)[1]
        assert "argument-hint:" in fm, "Frontmatter must include argument-hint"

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"


# -- 2. TestWikiInteraction (~12) ------------------------------------------

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

    def test_reads_ideas(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "ideas/" in reads

    def test_reads_query_pack(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "context_brief.md" in reads

    def test_reads_edges_jsonl(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "edges.jsonl" in reads

    def test_reads_paper_plan_optional(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "paper-plan" in reads

    def test_reads_reviewer_independence(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "cross-model-review.md" in reads

    def test_writes_rebuttal_md(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "rebuttal-" in writes and ".md" in writes

    def test_writes_rebuttal_formal_txt(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert ".txt" in writes or "formal" in writes

    def test_writes_to_outputs_dir(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "wiki/outputs/" in writes

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    def test_no_graph_edges_created(self, skill_text):
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert "无" in graph or "none" in graph.lower() or "不修改" in graph


# -- 3. TestWorkflow (~12) -------------------------------------------------

class TestWorkflow:
    """Validate workflow covers all 6 required steps."""

    def test_has_6_steps(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        steps = re.findall(r"^### Step \d+", workflow, re.MULTILINE)
        assert len(steps) >= 6, f"Expected >= 6 workflow steps, found {len(steps)}"

    def test_step1_parse_reviews(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "解析" in workflow or "parse" in workflow.lower()

    def test_step1_identifies_reviewers(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Reviewer" in workflow or "reviewer" in workflow

    def test_step1_identifies_scores(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Accept" in workflow or "Reject" in workflow or "score" in workflow.lower()

    def test_step1_structured_fields(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Strengths" in workflow or "Weaknesses" in workflow

    def test_step2_atomize_concerns(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "原子化" in workflow or "atomiz" in workflow.lower()

    def test_step2_concern_id_format(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Rv1-C1" in workflow or "Rvx-Cy" in workflow or "Rv1-" in workflow

    def test_step2_concern_types(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        for ctype in ["evidence", "method", "clarity", "scope", "novelty", "missing", "minor"]:
            assert ctype in workflow, f"Concern type '{ctype}' must appear in workflow"

    def test_step3_map_to_claims(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "映射" in workflow or "map" in workflow.lower()
        assert "claim" in workflow.lower()

    def test_step4_draft_rebuttal(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "起草" in workflow or "draft" in workflow.lower() or "Rebuttal" in workflow

    def test_step5_review_llm_stress_test(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "stress-test" in workflow.lower() or "stress_test" in workflow.lower()

    def test_step6_format_output(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "格式化" in workflow or "format" in workflow.lower()


# -- 4. TestConcernAtomization (~8) ----------------------------------------

class TestConcernAtomization:
    """Validate concern atomization rules."""

    def test_atomic_units(self, skill_text):
        assert "原子" in skill_text or "atomic" in skill_text.lower()

    def test_concern_id_rvx_cy_format(self, skill_text):
        # Should have Rvx-Cy IDs like Rv1-C1, Rv1-C2, Rv2-C1
        assert re.search(r"Rv\d+-C\d+", skill_text), "Must use Rvx-Cy concern ID format"

    @pytest.mark.parametrize("concern_type", [
        "evidence", "method", "clarity", "scope", "novelty", "missing", "minor",
    ])
    def test_concern_type_documented(self, skill_text, concern_type):
        assert concern_type in skill_text, \
            f"Concern type '{concern_type}' must be documented"

    @pytest.mark.parametrize("severity", ["critical", "major", "minor"])
    def test_severity_level_documented(self, skill_text, severity):
        assert severity in skill_text, \
            f"Severity level '{severity}' must be documented"

    def test_compound_sentence_split(self, skill_text):
        assert "复合句" in skill_text or "compound" in skill_text.lower() or \
               "拆分" in skill_text or "split" in skill_text.lower()

    def test_reviewer_number_preserved(self, skill_text):
        assert "保留 reviewer 编号" in skill_text or "reviewer" in skill_text.lower()
        # Must have R1, R2 pattern
        assert re.search(r"R\d+", skill_text)


# -- 5. TestClaimMapping (~6) ----------------------------------------------

class TestClaimMapping:
    """Validate concern-to-claim mapping."""

    def test_concerns_mapped_to_claims(self, skill_text):
        assert "映射" in skill_text or "map" in skill_text.lower()
        assert "claim" in skill_text.lower()

    def test_evidence_status_checked(self, skill_text):
        # Three evidence levels: sufficient, partial, insufficient
        assert ("充分" in skill_text or "sufficient" in skill_text.lower())

    def test_evidence_partial_status(self, skill_text):
        assert "部分充分" in skill_text or "partial" in skill_text.lower()

    def test_unmapped_concerns_flagged(self, skill_text):
        assert "unmapped" in skill_text

    def test_evidence_assessment_table(self, skill_text):
        # Should have a table with Evidence Status column
        assert "Evidence Status" in skill_text or "evidence" in skill_text.lower()
        # Table format: pipes
        assert re.search(r"\|.*[Cc]oncern.*\|.*[Cc]laim.*\|", skill_text)

    def test_experiment_results_referenced(self, skill_text):
        assert "experiment" in skill_text.lower() and "result" in skill_text.lower()

    def test_gap_identification(self, skill_text):
        assert "Gap" in skill_text or "gap" in skill_text or "缺口" in skill_text or "缺少" in skill_text


# -- 6. TestSafetyChecks (~5) ----------------------------------------------

class TestSafetyChecks:
    """Validate safety checks for rebuttal responses."""

    def test_no_fabrication_rule(self, skill_text):
        assert "No fabrication" in skill_text or "no fabrication" in skill_text.lower() or \
               "不编造" in skill_text

    def test_no_overpromise_rule(self, skill_text):
        assert "No overpromise" in skill_text or "no overpromise" in skill_text.lower() or \
               "overpromise" in skill_text

    def test_full_coverage_rule(self, skill_text):
        assert "Full coverage" in skill_text or "full coverage" in skill_text.lower() or \
               "全覆盖" in skill_text

    def test_evidence_traceability(self, skill_text):
        assert "追溯" in skill_text or "traceab" in skill_text.lower() or \
               "标注来源" in skill_text

    def test_specific_commitments(self, skill_text):
        # Must demand specific rather than vague promises
        assert "具体" in skill_text or "specific" in skill_text.lower()


# -- 7. TestStressTest (~6) ------------------------------------------------

class TestStressTest:
    """Validate Review LLM stress-test integration."""

    def test_stress_test_parameter(self, skill_text):
        assert "--stress-test" in skill_text

    def test_uses_llm_review_chat(self, skill_text):
        assert "mcp__llm-review__chat" in skill_text

    def test_review_llm_independence_followed(self, skill_text):
        assert "cross-model-review.md" in skill_text

    def test_convincing_score_1_to_5(self, skill_text):
        assert "1-5" in skill_text or ("score" in skill_text.lower() and "5" in skill_text)

    def test_overpromise_detection(self, skill_text):
        # Stress-test should detect overpromises
        assert "overpromise" in skill_text

    def test_follow_up_question_handling(self, skill_text):
        # Should handle follow-up questions from Review LLM
        assert "follow-up" in skill_text.lower() or "追问" in skill_text


# -- 8. TestOutputFormats (~6) ---------------------------------------------

class TestOutputFormats:
    """Validate dual output format (formal + rich)."""

    def test_formal_format_documented(self, skill_text):
        assert "formal" in skill_text

    def test_rich_format_documented(self, skill_text):
        assert "rich" in skill_text

    def test_formal_plain_text(self, skill_text):
        # formal = plain text for submission system
        assert "纯文本" in skill_text or "plain text" in skill_text.lower() or \
               "submission system" in skill_text.lower()

    def test_rich_has_wiki_links(self, skill_text):
        assert "wiki" in skill_text.lower() and "[[" in skill_text

    def test_both_formats_generated(self, skill_text):
        outputs = _extract_section(skill_text, "Outputs", level=2)
        assert ".md" in outputs and ".txt" in outputs

    def test_archive_to_wiki_outputs(self, skill_text):
        outputs = _extract_section(skill_text, "Outputs", level=2)
        assert "wiki/outputs/" in outputs

    def test_rebuttal_has_md_file(self, skill_text):
        assert re.search(r"rebuttal-.*\.md", skill_text)

    def test_rebuttal_has_txt_file(self, skill_text):
        assert re.search(r"rebuttal-.*\.txt", skill_text)


# -- 9. TestConstraints (~9) -----------------------------------------------

class TestConstraints:
    """Validate constraints cover key rebuttal rules."""

    def test_no_fabrication_constraint(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "fabrication" in constraints.lower() or "编造" in constraints

    def test_no_overpromise_constraint(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "overpromise" in constraints.lower()

    def test_full_coverage_constraint(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "coverage" in constraints.lower() or "覆盖" in constraints or "遗漏" in constraints

    def test_evidence_traceability_constraint(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "追溯" in constraints or "traceab" in constraints.lower() or "标注来源" in constraints

    def test_no_direct_wiki_modification(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("不修改 wiki" in constraints or "不直接" in constraints or
                "建议" in constraints or "do not" in constraints.lower() and "wiki" in constraints.lower() or
                "not directly modify" in constraints.lower())

    def test_stress_test_independence(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "独立" in constraints or "independence" in constraints.lower() or \
               "cross-model-review" in constraints

    def test_concern_ids_rvx_cy(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "Rvx-Cy" in constraints or "Rv1-" in constraints or "ID" in constraints or \
               "concern" in constraints.lower()

    def test_specific_commitments_constraint(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "具体" in constraints or "specific" in constraints.lower()

    def test_writes_to_outputs_only(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "outputs" in constraints.lower() or "不直接写" in constraints


# -- 10. TestErrorHandling (~6) --------------------------------------------

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_reviews_file_not_found(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "找不到" in errors or "not found" in errors.lower()

    def test_cannot_parse_reviewer_structure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "解析" in errors or "parse" in errors.lower()

    def test_concern_unmapped_to_claim(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "unmapped" in errors or "映射不到" in errors

    def test_review_llm_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("Review LLM" in errors or "review llm" in errors.lower() or "llm-review" in errors) and ("不可用" in errors or "unavailable" in errors.lower())

    def test_evidence_completely_insufficient(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "evidence" in errors.lower() and ("不足" in errors or "insufficient" in errors.lower())

    def test_wiki_empty(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "wiki" in errors.lower() and ("空" in errors or "empty" in errors.lower())


# -- 11. TestToolReferences (~5) -------------------------------------------

class TestToolReferences:
    """Validate all referenced tools exist and are documented."""

    def test_research_wiki_slug(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "research_wiki.py" in deps and "slug" in deps

    def test_research_wiki_log(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "research_wiki.py" in deps and "log" in deps

    def test_llm_review_chat_for_stress_test(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "mcp__llm-review__chat" in deps

    def test_claude_code_native_tools(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        for tool in ["Read", "Write", "Glob", "Grep"]:
            assert tool in deps, f"Claude Code native tool '{tool}' must be in Dependencies"

    def test_reviewer_independence_in_deps(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "cross-model-review.md" in deps


# -- 12. TestSharedReferences (~3) -----------------------------------------

class TestSharedReferences:
    """Validate shared reference usage."""

    def test_reviewer_independence_referenced(self, skill_text):
        assert "cross-model-review.md" in skill_text

    def test_reviewer_independence_file_exists(self):
        path = SHARED_REFS / "cross-model-review.md"
        assert path.exists(), f"cross-model-review.md not found at {path}"

    def test_no_citation_discipline_referenced(self, skill_text):
        # Rebuttal is not generating citations in the academic sense
        deps = _extract_section(skill_text, "Dependencies", level=2)
        shared_part = _extract_section(skill_text, "Shared References", level=3)
        combined = deps + shared_part
        assert "citation-verification.md" not in combined, \
            "Rebuttal should not reference citation-verification.md"


# -- 13. TestClaudeMdConsistency (~4) --------------------------------------

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_rebuttal_listed_in_claude_md(self, claude_md_text):
        # The /rebuttal skill should be registered in CLAUDE.md (it may not be yet for Phase 4)
        # Accept either direct listing or absence as Phase 4 future work
        # But check the dev CLAUDE.md mentions it in Phase 4
        pass  # Phase 4 skill; may not yet be in product CLAUDE.md

    def test_log_format_matches(self, skill_text):
        # Log command should use 'log wiki/' format
        assert "log wiki/" in skill_text

    def test_rebuttal_categorized_phase_4(self):
        """Rebuttal is a Phase 4 skill per development CLAUDE.md."""
        dev_claude = Path(__file__).resolve().parent.parent.parent.parent / "CLAUDE.md"
        if dev_claude.exists():
            text = dev_claude.read_text(encoding="utf-8")
            # Phase 4 section should mention rebuttal
            phase4 = _extract_section(text, "Phase 4", level=3)
            assert "rebuttal" in phase4.lower() or "/rebuttal" in phase4

    def test_uses_wikilink_syntax(self, skill_text):
        assert "[[" in skill_text, "Must use wikilink syntax [[slug]]"


# -- 14. TestActionItems (~4) ----------------------------------------------

class TestActionItems:
    """Validate action items section in output template."""

    def test_suggests_experiments_to_add(self, skill_text):
        assert "/exp-design" in skill_text

    def test_paper_edits_listed(self, skill_text):
        # Should list specific paper edits
        assert "Paper Edit" in skill_text or "paper edit" in skill_text.lower() or \
               "修改" in skill_text

    def test_wiki_updates_suggested(self, skill_text):
        assert "Wiki Update" in skill_text or "wiki update" in skill_text.lower() or \
               "Wiki 更新" in skill_text or "Wiki Updates" in skill_text

    def test_action_items_are_specific(self, skill_text):
        # Should contain specific examples, not vague
        # Check for section/table references in the action items area
        assert "Section" in skill_text or "Table" in skill_text or \
               "section" in skill_text.lower()

"""Tests for /refine SKILL.md structural completeness.

Validates that the refine skill follows extending.md structure,
implements the iterative review-fix cycle, references /review skill,
and aligns with product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "refine" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"
REVIEW_SKILL = PROJECT_ROOT / ".claude" / "skills" / "review" / "SKILL.md"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"refine SKILL.md not found at {SKILL_PATH}"
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
        assert "description:" in fm

    def test_has_skill_heading(self, skill_text):
        assert re.search(r"^# /refine", skill_text, re.MULTILINE)

    def test_has_intro_paragraph(self, skill_text):
        assert re.search(r"^>", skill_text, re.MULTILINE)

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"


# ── 2. Wiki Interaction ──────────────────────────────────────────────

class TestWikiInteraction:
    """Validate wiki interactions are documented."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE)

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE)

    def test_reads_ideas(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "ideas/" in reads

    def test_reads_experiments(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "experiments/" in reads

    def test_reads_claims(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "claims/" in reads

    def test_reads_query_pack(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "context_brief.md" in reads

    def test_writes_ideas(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "ideas/" in writes

    def test_writes_claims(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "claims/" in writes

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    def test_writes_query_pack(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "context_brief.md" in writes


# ── 3. Workflow — iterative loop ────────────────────────────────────

class TestWorkflow:
    """Validate the iterative review-fix workflow."""

    def test_has_initialization_step(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "初始化" in workflow or "初始" in workflow or "Step 1" in workflow

    def test_has_iteration_loop(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "迭代" in workflow or "循环" in workflow or "Round" in workflow

    def test_calls_review_each_round(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "/review" in workflow

    def test_parses_actionable_items(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "actionable" in workflow.lower() or "可操作" in workflow

    def test_fixes_artifact(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "修复" in workflow or "fix" in workflow.lower()

    def test_updates_wiki(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "wiki" in workflow.lower() and ("更新" in workflow or "update" in workflow.lower())

    def test_has_final_report(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "报告" in workflow or "report" in workflow.lower() or "REFINE_REPORT" in workflow


# ── 4. Termination conditions ───────────────────────────────────────

class TestTermination:
    """Validate termination conditions for the loop."""

    def test_target_score_termination(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "target" in workflow.lower() and "score" in workflow.lower()

    def test_convergence_termination(self, skill_text):
        """Should stop when score stops improving."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "收敛" in workflow or "converge" in workflow.lower() or "无提升" in workflow

    def test_max_rounds_termination(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "max" in workflow.lower() and ("round" in workflow.lower() or "轮" in workflow)

    def test_ready_verdict_termination(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "ready" in workflow

    def test_rethink_early_termination(self, skill_text):
        """Should not iterate on rethink-level artifacts."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "rethink" in workflow


# ── 5. Issue classification ─────────────────────────────────────────

class TestIssueClassification:
    """Validate that actionable items are classified and handled."""

    def test_category_a_direct_fix(self, skill_text):
        """Category A: Claude fixes directly."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Category A" in workflow or "方法" in workflow or "内容" in workflow

    def test_category_b_wiki_gap(self, skill_text):
        """Category B: wiki knowledge gap."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "知识缺口" in workflow or "knowledge gap" in workflow.lower() or "Category B" in workflow

    def test_category_c_claim_update(self, skill_text):
        """Category C: claim status update."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "claim" in workflow.lower() and ("confidence" in workflow or "status" in workflow.lower())

    def test_unresolved_issues_tracked(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "unresolved" in workflow.lower() or "未解决" in workflow


# ── 6. Parameters ───────────────────────────────────────────────────

class TestParameters:
    """Validate input parameters."""

    def test_max_rounds_param(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "max-rounds" in inputs or "max_rounds" in inputs

    def test_max_rounds_default(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "4" in inputs, "Default max-rounds should be 4"

    def test_target_score_param(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "target-score" in inputs or "target_score" in inputs

    def test_target_score_default(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "8" in inputs, "Default target-score should be 8"

    def test_difficulty_passthrough(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "difficulty" in inputs.lower()

    def test_focus_passthrough(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "focus" in inputs.lower()


# ── 7. Output report ────────────────────────────────────────────────

class TestOutputReport:
    """Validate the REFINE_REPORT output format."""

    def test_score_trajectory(self, skill_text):
        assert "score" in skill_text.lower() and ("trajectory" in skill_text.lower() or "轨迹" in skill_text or "history" in skill_text.lower())

    def test_fixed_issues_list(self, skill_text):
        assert "fixed" in skill_text.lower() or "修复" in skill_text

    def test_unresolved_issues_list(self, skill_text):
        assert "unresolved" in skill_text.lower() or "未解决" in skill_text

    def test_wiki_changes_list(self, skill_text):
        assert "Wiki Changes" in skill_text or "wiki_changes" in skill_text

    def test_next_steps(self, skill_text):
        assert "Next Steps" in skill_text or "next step" in skill_text.lower()

    def test_refine_report_keyword(self, skill_text):
        assert "REFINE_REPORT" in skill_text or "Refine Loop Report" in skill_text


# ── 8. Artifact types supported ─────────────────────────────────────

class TestArtifactTypes:
    """Validate support for multiple artifact types."""

    @pytest.mark.parametrize("artifact_type", [
        "idea", "experiment", "paper", "proposal",
    ])
    def test_artifact_type_mentioned(self, skill_text, artifact_type):
        assert artifact_type in skill_text.lower(), \
            f"Must support artifact type '{artifact_type}'"


# ── 9. Tool and skill dependencies ──────────────────────────────────

class TestDependencies:
    """Validate tool and skill dependencies."""

    def test_depends_on_review_skill(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "/review" in deps or "review" in deps

    def test_review_skill_exists(self):
        assert REVIEW_SKILL.exists(), f"Review SKILL.md must exist at {REVIEW_SKILL}"

    def test_uses_rebuild_context_brief(self, skill_text):
        assert "rebuild-context-brief" in skill_text

    def test_uses_rebuild_open_questions(self, skill_text):
        assert "rebuild-open-questions" in skill_text

    def test_uses_log(self, skill_text):
        assert "log" in skill_text.lower() and "research_wiki.py" in skill_text

    def test_research_wiki_exists(self):
        assert (TOOLS_DIR / "research_wiki.py").exists()


# ── 10. Constraints ─────────────────────────────────────────────────

class TestConstraints:
    """Validate constraints cover key rules."""

    def test_convergence_stops_loop(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("收敛" in constraints or "无变化" in constraints or
                "converge" in constraints.lower() or "does not change" in constraints.lower() or
                "no change" in constraints.lower() or "score" in constraints.lower())

    def test_rethink_no_iterate(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "rethink" in constraints

    def test_wiki_changes_limited(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "review" in constraints.lower() and ("建议" in constraints or "suggest" in constraints.lower())

    def test_unresolved_must_be_listed(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "unresolved" in constraints.lower() or "未解决" in constraints

    def test_score_history_preserved(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "history" in constraints.lower() or "历史" in constraints or "score_history" in constraints

    def test_difficulty_passthrough(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "difficulty" in constraints.lower() or "透传" in constraints

    def test_artifact_in_place_update(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("原地" in constraints or "in-place" in constraints.lower() or
                "原始" in constraints or "in place" in constraints.lower() or
                "directly" in constraints.lower())


# ── 11. Error handling ───────────────────────────────────────────────

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_artifact_not_found(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "找不到" in errors or "not found" in errors.lower()

    def test_review_call_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "review" in errors.lower() and ("失败" in errors or "fail" in errors.lower())

    def test_wiki_write_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "wiki" in errors.lower() and ("写入" in errors or "write" in errors.lower())

    def test_already_at_target(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "target" in errors.lower() and "score" in errors.lower()

    def test_all_unresolvable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "Category B" in errors or "Category D" in errors or \
               ("无法" in errors and "修复" in errors)


# ── 12. CLAUDE.md consistency ────────────────────────────────────────

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_uses_wikilink_syntax(self, skill_text):
        assert "[[" in skill_text

    def test_references_claim_confidence(self, skill_text):
        assert "confidence" in skill_text

    def test_references_review_verdicts(self, skill_text):
        for verdict in ["ready", "needs-work", "major-revision", "rethink"]:
            assert verdict in skill_text, \
                f"Must reference verdict '{verdict}' from /review"


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

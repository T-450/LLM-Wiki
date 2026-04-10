"""Tests for /review SKILL.md structural completeness.

Validates that the review skill follows extending.md structure,
references correct MCP servers, documents wiki interactions,
supports difficulty/focus parameters, and aligns with product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "review" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"review SKILL.md not found at {SKILL_PATH}"
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
        assert re.search(r"^# /review", skill_text, re.MULTILINE), \
            "SKILL.md must have '# /review' heading"

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
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE)

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE)

    def test_reads_papers(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "papers/" in reads

    def test_reads_concepts(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "concepts/" in reads

    def test_reads_claims(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "claims/" in reads

    def test_reads_experiments(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "experiments/" in reads

    def test_reads_query_pack(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "context_brief.md" in reads

    def test_reads_gap_map(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "open_questions.md" in reads

    def test_reads_reviewer_independence(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "cross-model-review.md" in reads

    def test_writes_nothing(self, skill_text):
        """Review is read-only — must not write to wiki."""
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "无" in writes or "不直接修改" in writes or "none" in writes.lower()

    def test_no_graph_edges(self, skill_text):
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert "无" in graph or "none" in graph.lower()


# ── 3. Workflow — 4 steps ────────────────────────────────────────────


class TestWorkflow:
    """Validate workflow covers all 4 required steps."""

    def test_has_at_least_4_steps(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        steps = re.findall(r"^### Step \d+", workflow, re.MULTILINE)
        assert len(steps) >= 4, f"Expected >= 4 workflow steps, found {len(steps)}"

    def test_workflow_contains_all_keywords(self, skill_text, review_workflow_keywords):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        for keyword in review_workflow_keywords:
            assert keyword in workflow, \
                f"Workflow missing content containing '{keyword}'"

    def test_step1_loads_context(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "context_brief.md" in workflow
        assert "open_questions.md" in workflow

    def test_step2_llm_review(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "mcp__llm-review__chat" in workflow

    def test_step3_multi_turn(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "mcp__llm-review__chat-reply" in workflow

    def test_step3_max_rounds(self, skill_text):
        """Multi-turn dialogue should have max 3 rounds."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "3" in workflow and ("轮" in workflow or "round" in workflow.lower())

    def test_reviewer_system_prompt(self, skill_text):
        """Must build reviewer system prompt based on --focus."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "system prompt" in workflow.lower() or "system" in workflow.lower()


# ── 4. Difficulty levels ──────────────────────────────────────────────

class TestDifficultyLevels:
    """Validate support for 3 difficulty levels."""

    @pytest.mark.parametrize("level", ["standard", "hard", "adversarial"])
    def test_difficulty_level_documented(self, skill_text, level):
        assert level in skill_text, \
            f"Difficulty level '{level}' must be documented"

    def test_standard_is_single_round(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "standard" in inputs and (
            "单轮" in inputs or "single-round" in inputs.lower() or "single round" in inputs.lower()
        )

    def test_hard_is_multi_round(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "hard" in inputs and (
            "多轮" in inputs or "multi-round" in inputs.lower() or "3" in inputs
        )

    def test_adversarial_searches_fatal_flaws(self, skill_text):
        assert "致命" in skill_text or "fatal" in skill_text.lower()

    def test_default_difficulty(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "standard" in inputs, "Default difficulty should be standard"


# ── 5. Focus modes ───────────────────────────────────────────────────

class TestFocusModes:
    """Validate support for 4 focus modes."""

    @pytest.mark.parametrize("focus", ["method", "evidence", "writing", "completeness"])
    def test_focus_mode_documented(self, skill_text, focus):
        assert focus in skill_text, \
            f"Focus mode '{focus}' must be documented"

    def test_method_focus_checks(self, skill_text):
        assert "correctness" in skill_text.lower() or "正确性" in skill_text

    def test_evidence_focus_checks(self, skill_text):
        assert "experimental" in skill_text.lower() or "实验" in skill_text

    def test_writing_focus_checks(self, skill_text):
        assert "clarity" in skill_text.lower() or "清晰" in skill_text

    def test_completeness_focus_checks(self, skill_text):
        assert "ablation" in skill_text.lower() or "baseline" in skill_text.lower()


# ── 6. Output structure ──────────────────────────────────────────────

class TestOutputStructure:
    """Validate the review report output format."""

    def test_score_range_1_to_10(self, skill_text):
        assert "1-10" in skill_text, "Must document 1-10 scoring range"

    @pytest.mark.parametrize("verdict", ["ready", "needs-work", "major-revision", "rethink"])
    def test_verdict_options(self, skill_text, verdict):
        assert verdict in skill_text, \
            f"Verdict option '{verdict}' must be documented"

    def test_strengths_in_output(self, skill_text):
        outputs = _extract_section(skill_text, "Outputs", level=2)
        assert "Strengths" in outputs or "strengths" in skill_text.lower()

    def test_weaknesses_in_output(self, skill_text):
        outputs = _extract_section(skill_text, "Outputs", level=2)
        assert "Weaknesses" in outputs or "weaknesses" in skill_text.lower()

    def test_actionable_suggestions(self, skill_text):
        assert "Actionable" in skill_text or "actionable" in skill_text

    def test_wiki_entity_mapping(self, skill_text):
        assert "Wiki Entity Mapping" in skill_text or "wiki_entity_mapping" in skill_text


# ── 7. Wiki Entity Mapping ───────────────────────────────────────────

class TestWikiEntityMapping:
    """Validate that review output maps to wiki entities."""

    def test_claims_needing_support(self, skill_text):
        assert "claims" in skill_text.lower() and ("support" in skill_text.lower() or "加强" in skill_text)

    def test_gaps_identified(self, skill_text):
        assert "gap" in skill_text.lower() and ("identified" in skill_text.lower() or "发现" in skill_text)

    def test_suggested_wiki_updates(self, skill_text):
        assert "wiki" in skill_text.lower() and ("update" in skill_text.lower() or "更新" in skill_text)

    def test_claim_confidence_referenced(self, skill_text):
        assert "confidence" in skill_text, "Must reference claim confidence in entity mapping"


# ── 8. Review LLM integration ─────────────────────────────────────────────

class TestLLMReviewIntegration:
    """Validate Review LLM MCP server integration."""

    def test_llm_review_chat_referenced(self, skill_text):
        assert "mcp__llm-review__chat" in skill_text

    def test_llm_review_chat_reply_referenced(self, skill_text):
        assert "mcp__llm-review__chat-reply" in skill_text

    def test_reviewer_independence_referenced(self, skill_text):
        assert "cross-model-review.md" in skill_text

    def test_reviewer_independence_file_exists(self):
        path = SHARED_REFS / "cross-model-review.md"
        assert path.exists(), f"cross-model-review.md not found at {path}"


# ── 9. Constraints ───────────────────────────────────────────────────

REQUIRED_CONSTRAINT_KEYWORDS = [
    "独立",             # reviewer independence
    "不修改" if True else "不直接修改",  # no wiki writes
    "justification",    # score must have justification
    "fix",              # weakness must have fix
    "Wiki Entity Mapping",  # must include entity mapping
]


class TestConstraints:
    """Validate constraints cover key rules."""

    def test_reviewer_independence_constraint(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "独立" in constraints or "independence" in constraints.lower()

    def test_no_wiki_modification(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert (
            "不修改" in constraints or "不直接修改" in constraints
            or "not modify" in constraints.lower() or "read-only" in constraints.lower()
            or "no wiki" in constraints.lower()
        )

    def test_score_justification_required(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "justification" in constraints or "理由" in constraints

    def test_weakness_must_have_fix(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "fix" in constraints.lower() or "修复" in constraints

    def test_entity_mapping_required(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "mapping" in constraints.lower() or "映射" in constraints

    def test_max_3_rounds(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "3" in constraints and ("轮" in constraints or "round" in constraints.lower())

    def test_wikilink_syntax(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "[[" in constraints or "wikilink" in constraints.lower()


# ── 10. Error handling ────────────────────────────────────────────────

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_artifact_not_found(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "找不到" in errors or "not found" in errors.lower()

    def test_review_llm_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("Review LLM" in errors or "review llm" in errors.lower() or "llm-review" in errors) and ("不可用" in errors or "unavailable" in errors.lower())

    def test_degraded_mode(self, skill_text):
        """Should degrade to single-model review when Review LLM is down."""
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "降级" in errors or "degrade" in errors.lower() or "single-model" in errors

    def test_empty_wiki(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "wiki" in errors.lower() and ("空" in errors or "empty" in errors.lower())

    def test_artifact_too_long(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "长" in errors or "long" in errors.lower() or "上下文" in errors


# ── 11. CLAUDE.md consistency ─────────────────────────────────────────

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_skill_uses_wikilink_syntax(self, skill_text):
        assert "[[" in skill_text, "Must use wikilink syntax [[slug]]"

    def test_claim_confidence_range(self, skill_text):
        """Should reference claim confidence in entity mapping."""
        assert "confidence" in skill_text

    def test_severity_levels_documented(self, skill_text):
        """Should classify weaknesses by severity."""
        for level in ["critical", "major", "minor"]:
            assert level.lower() in skill_text.lower() or \
                   level.capitalize() in skill_text, \
                f"Severity level '{level}' must be documented"


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

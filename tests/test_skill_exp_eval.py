"""Tests for /exp-eval SKILL.md structural completeness.

Validates that the exp-eval skill follows extending.md structure,
implements Review LLM verdict gate with 4 judgment paths, documents wiki interactions
for claims/ideas/experiments updates, and aligns with product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "exp-eval" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"exp-eval SKILL.md not found at {SKILL_PATH}"
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
        assert re.search(r"^# /exp-eval", skill_text, re.MULTILINE), \
            "SKILL.md must have '# /exp-eval' heading"

    def test_has_intro_paragraph(self, skill_text):
        assert re.search(r"^>", skill_text, re.MULTILINE), \
            "SKILL.md must have intro paragraph (blockquote)"

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"


# ── 2. Wiki Interaction ─────────────────────────────────────────────────

class TestWikiInteraction:
    """Validate wiki interaction documentation."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE)

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE)

    def test_has_graph_edges_subsection(self, skill_text):
        assert re.search(r"^###\s+Graph edges", skill_text, re.MULTILINE)

    def test_reads_experiments(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "experiments/" in reads

    def test_reads_claims(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "claims/" in reads

    def test_reads_ideas(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "ideas/" in reads

    def test_reads_query_pack(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "context_brief.md" in reads

    def test_reads_reviewer_independence(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "cross-model-review.md" in reads

    def test_writes_claims(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "claims/" in writes

    def test_writes_ideas(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "ideas/" in writes

    def test_writes_experiments(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "experiments/" in writes

    def test_writes_edges(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "edges.jsonl" in writes

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    def test_graph_edge_supports(self, skill_text):
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert "supports" in graph

    def test_graph_edge_invalidates(self, skill_text):
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert "invalidates" in graph


# ── 3. Workflow — 4 steps ──────────────────────────────────────────────

EXPECTED_WORKFLOW_KEYWORDS = [
    ("加载上下文", "load context"),  # Step 1: load context (en) / 加载上下文 (zh)
    ("Review LLM", "review llm"),    # Step 2: Review LLM verdict
    ("综合评估", "synthesis"),       # Step 3: Claude synthesis (en) / 综合评估 (zh)
    ("更新 Wiki", "update wiki"),    # Step 4: update wiki (en) / 更新 Wiki (zh)
]


class TestWorkflow:
    """Validate workflow covers all 4 required steps."""

    def test_has_at_least_4_steps(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        steps = re.findall(r"^### Step \d+", workflow, re.MULTILINE)
        assert len(steps) >= 4, f"Expected >= 4 workflow steps, found {len(steps)}"

    @pytest.mark.parametrize("zh_kw,en_kw", EXPECTED_WORKFLOW_KEYWORDS)
    def test_workflow_contains_keyword(self, skill_text, zh_kw, en_kw):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert zh_kw in workflow or en_kw in workflow.lower(), \
            f"Workflow missing content containing '{zh_kw}' or '{en_kw}'"

    def test_step1_reads_experiment(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "experiment" in workflow.lower() and "target_claim" in workflow

    def test_step1_reads_other_experiments(self, skill_text):
        """Should load other experiments on the same claim."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "其他实验" in workflow or "other experiment" in workflow.lower() or "同一 claim" in workflow

    def test_step2_review_llm_verdict(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "mcp__llm-review__chat" in workflow

    def test_step2_impartial_judge(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "impartial" in workflow.lower() or "公正" in workflow

    def test_step3_claude_independent(self, skill_text):
        """Claude should also form independent judgment."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "独立" in workflow or "independent" in workflow.lower()

    def test_step3_composing_verdicts(self, skill_text):
        """Should compose Claude and Review LLM verdicts."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "综合" in workflow or "compos" in workflow.lower()


# ── 4. Verdict paths ───────────────────────────────────────────────────

class TestVerdictPaths:
    """Validate all 4 verdict paths are documented."""

    @pytest.mark.parametrize("verdict", [
        "supported", "partially_supported", "not_supported", "inconclusive",
    ])
    def test_verdict_path_exists(self, skill_text, verdict):
        assert verdict.upper() in skill_text or verdict in skill_text, \
            f"Verdict path '{verdict}' must be documented"

    def test_supported_increases_confidence(self, skill_text):
        # Look in the supported section for confidence increase
        assert "confidence" in skill_text and ("↑" in skill_text or "+" in skill_text)

    def test_not_supported_decreases_confidence(self, skill_text):
        assert "confidence" in skill_text and ("↓" in skill_text or "-" in skill_text)

    def test_supported_validates_idea(self, skill_text):
        assert "validated" in skill_text

    def test_not_supported_fails_idea(self, skill_text):
        assert "failed" in skill_text and "failure_reason" in skill_text

    def test_partially_suggests_more_experiments(self, skill_text):
        assert "补充实验" in skill_text or "supplementary" in skill_text.lower() or \
               "follow-up" in skill_text.lower()

    def test_inconclusive_suggests_debug(self, skill_text):
        assert "debug" in skill_text.lower() or "调试" in skill_text

    def test_supported_suggests_paper_plan(self, skill_text):
        assert "/paper-plan" in skill_text

    def test_not_supported_suggests_idea_generation(self, skill_text):
        assert "/ideate" in skill_text


# ── 5. Claim updates ───────────────────────────────────────────────────

class TestClaimUpdates:
    """Validate claim update mechanics."""

    def test_updates_confidence(self, skill_text):
        assert "confidence" in skill_text

    def test_updates_status(self, skill_text):
        for status in ["supported", "weakly_supported", "challenged"]:
            assert status in skill_text, \
                f"Claim status '{status}' must be referenced"

    def test_appends_evidence(self, skill_text):
        assert "evidence" in skill_text and ("追加" in skill_text or "append" in skill_text.lower())

    def test_evidence_has_strength(self, skill_text):
        assert "strength" in skill_text.lower()

    def test_evidence_has_type(self, skill_text):
        """Evidence type should be supports or invalidates."""
        assert "supports" in skill_text and "invalidates" in skill_text


# ── 6. Idea updates ────────────────────────────────────────────────────

class TestIdeaUpdates:
    """Validate idea status updates based on verdict."""

    def test_idea_validated_on_supported(self, skill_text):
        assert "validated" in skill_text

    def test_idea_failed_on_not_supported(self, skill_text):
        assert "failed" in skill_text

    def test_failure_reason_recorded(self, skill_text):
        assert "failure_reason" in skill_text

    def test_failure_reason_is_anti_repetition(self, skill_text):
        assert "anti-repetition" in skill_text.lower() or "反重复" in skill_text


# ── 7. Review LLM integration ────────────────────────────────────────────────

class TestLLMReviewIntegration:
    """Validate Review LLM MCP server integration for impartial verdict."""

    def test_llm_review_chat_referenced(self, skill_text):
        assert "mcp__llm-review__chat" in skill_text

    def test_reviewer_independence_referenced(self, skill_text):
        assert "cross-model-review.md" in skill_text

    def test_reviewer_independence_file_exists(self):
        path = SHARED_REFS / "cross-model-review.md"
        assert path.exists(), f"cross-model-review.md not found at {path}"

    def test_no_claude_prejudgment_sent(self, skill_text):
        """cross-model-review: must not send Claude's verdict to Review LLM."""
        assert "不向" in skill_text or "independence" in skill_text.lower() or \
               "预判" in skill_text

    def test_conservative_default(self, skill_text):
        """When verdicts disagree, take the more conservative one."""
        assert "保守" in skill_text or "conservative" in skill_text.lower()


# ── 8. Tool references ──────────────────────────────────────────────────

REQUIRED_TOOL_COMMANDS = [
    "add-edge",
    "rebuild-context-brief",
    "rebuild-open-questions",
    "log",
]


class TestToolReferences:
    """Validate all referenced tools exist."""

    @pytest.mark.parametrize("command", REQUIRED_TOOL_COMMANDS)
    def test_tool_command_referenced(self, skill_text, command):
        assert command in skill_text, \
            f"Tool command '{command}' must be referenced in SKILL.md"

    def test_research_wiki_tool_exists(self):
        assert (TOOLS_DIR / "research_wiki.py").exists()

    def test_tools_called_via_bash(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "research_wiki.py" in deps


# ── 9. Constraints ──────────────────────────────────────────────────────

class TestConstraints:
    """Validate constraints cover key rules."""

    def test_only_completed_experiments(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "completed" in constraints

    def test_reviewer_independence(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "独立" in constraints or "independence" in constraints.lower()

    def test_confidence_range(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "0.0" in constraints or "0.0-1.0" in constraints or "1.0" in constraints

    def test_failure_reason_specific(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "failure_reason" in constraints and ("具体" in constraints or "specific" in constraints.lower())

    def test_no_claim_deletion(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert ("不直接删除" in constraints or "不删除" in constraints or
                "never delete" in constraints.lower() or "do not delete" in constraints.lower() or
                "No deletion" in constraints or "not delete" in constraints.lower())

    def test_graph_edges_via_tool(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "research_wiki.py" in constraints or "edges.jsonl" in constraints

    def test_conservative_on_disagreement(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "保守" in constraints or "conservative" in constraints.lower()

    def test_considers_all_experiments(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "所有实验" in constraints or "all experiment" in constraints.lower() or \
               "其他实验" in constraints or "综合" in constraints


# ── 10. Error handling ───────────────────────────────────────────────────

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_experiment_not_found(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "找不到" in errors or "not found" in errors.lower()

    def test_experiment_not_completed(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "未完成" in errors or "not completed" in errors.lower() or "status" in errors

    def test_target_claim_missing(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "claim" in errors.lower() and ("不存在" in errors or "not exist" in errors.lower() or "创建" in errors)

    def test_review_llm_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("Review LLM" in errors or "review llm" in errors.lower() or "llm-review" in errors) and ("不可用" in errors or "unavailable" in errors.lower())

    def test_review_llm_degraded_mode(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "降级" in errors or "single-model" in errors

    def test_linked_idea_missing(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "idea" in errors.lower() and ("不存在" in errors or "not exist" in errors.lower() or "跳过" in errors)

    def test_results_data_missing(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "Results" in errors or "结果" in errors


# ── 11. CLAUDE.md consistency ────────────────────────────────────────────

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_skill_listed_in_claude_md(self, claude_md_text):
        assert "exp-eval" in claude_md_text, \
            "/exp-eval must be listed in product CLAUDE.md skills table"

    def test_uses_wikilink_syntax(self, skill_text):
        assert "[[" in skill_text, "Must use wikilink syntax [[slug]]"

    def test_claim_status_values(self, skill_text):
        """Status values must match CLAUDE.md claim template."""
        for status in ["proposed", "weakly_supported", "supported", "challenged", "deprecated"]:
            assert status in skill_text, \
                f"Claim status '{status}' must be referenced"

    def test_edge_types_valid(self, skill_text):
        """supports and invalidates must be valid edge types per CLAUDE.md."""
        valid_types = {
            "extends", "contradicts", "supports", "inspired_by",
            "tested_by", "invalidates", "supersedes", "addresses_gap", "derived_from",
        }
        graph = _extract_section(skill_text, "Graph edges", level=3)
        found_types = re.findall(r"`(\w+)`", graph)
        valid_found = [t for t in found_types if t in valid_types]
        assert len(valid_found) >= 2, "Must reference at least supports and invalidates edge types"

    def test_log_format(self, skill_text):
        assert "log wiki/" in skill_text


# ── 12. Output report ──────────────────────────────────────────────────

class TestOutputReport:
    """Validate the verdict report format."""

    def test_report_includes_verdict(self, skill_text):
        assert "VERDICT_REPORT" in skill_text or "Verdict Report" in skill_text

    def test_report_includes_judge_table(self, skill_text):
        assert "Claude" in skill_text and ("Review LLM" in skill_text or "llm-review" in skill_text.lower()) and "Final" in skill_text

    def test_report_includes_wiki_changes(self, skill_text):
        assert "Wiki Changes" in skill_text or "wiki changes" in skill_text.lower()

    def test_report_includes_graph_edges(self, skill_text):
        assert "Graph Edges" in skill_text or "graph edge" in skill_text.lower()

    def test_report_includes_concerns(self, skill_text):
        assert "Concerns" in skill_text or "concerns" in skill_text

    def test_report_includes_next_steps(self, skill_text):
        assert "Next Steps" in skill_text or "next step" in skill_text.lower()


# ── 13. Auto mode ──────────────────────────────────────────────────────

class TestAutoMode:
    """Validate --auto mode for pipeline integration."""

    def test_auto_flag_documented(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "--auto" in inputs

    def test_auto_skips_confirmation(self, skill_text):
        assert "确认" in skill_text or "confirm" in skill_text.lower()

    def test_auto_for_pipeline(self, skill_text):
        assert "/research" in skill_text


# ── Helpers ────────────────────────────────────────────────────────────

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

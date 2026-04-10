"""Tests for /exp-run SKILL.md structural completeness.

Validates that the exp-run skill follows extending.md structure,
covers 4 phases across three run modes (deploy / collect / full),
documents wiki interactions, and aligns with product CLAUDE.md.

Three modes:
  - deploy (default): Phase 1+2 only, returns after launching experiment
  - --collect: Phase 3+4 only, checks status and collects results
  - --full: all 4 phases (for quick local experiments)
  --check is a backward-compatible alias for --collect.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "exp-run" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"exp-run SKILL.md not found at {SKILL_PATH}"
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
        assert re.search(r"^# /exp-run", skill_text, re.MULTILINE), \
            "SKILL.md must have '# /exp-run' heading"

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

    def test_reads_papers(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "papers/" in reads

    def test_writes_experiments(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "experiments/" in writes

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    def test_no_graph_edges_created(self, skill_text):
        """exp-run should NOT create graph edges (done in exp-design)."""
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert "无" in graph or "已在" in graph or "not" in graph.lower() or "none" in graph.lower()

    def test_does_not_modify_claims(self, skill_text):
        """Claims update is /exp-eval's responsibility."""
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "不修改 claims" in constraints or "claims" in constraints.lower()


# ── 3. Workflow — 4 phases ─────────────────────────────────────────────

EXPECTED_PHASE_KEYWORDS = [
    "Prepare",          # Phase 1: prepare (en) / 准备 (zh)
    "Deploy",           # Phase 2: deploy (en) / 部署 (zh)
    "Monitor",          # Phase 3: monitor (en) / 监控 (zh)
    "Collect",          # Phase 4: collect results (en) / 收集 (zh)
]


class TestWorkflow:
    """Validate workflow covers all 4 required phases across the 3 modes."""

    def test_has_4_phases(self, skill_text):
        # Phases use **Phase N:** bold format (not ### headings) to avoid
        # interfering with _extract_section's level-2 heading stop condition
        phases = re.findall(r"\*\*Phase \d+[:\s]", skill_text)
        assert len(phases) >= 4, f"Expected >= 4 workflow phases, found {len(phases)}"

    def test_phases_1_2_in_deploy_mode(self, skill_text):
        """Phase 1 (prepare) and Phase 2 (deploy) belong to deploy mode."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Phase 1" in workflow and "Phase 2" in workflow

    def test_phases_3_4_in_collect_mode(self, skill_text):
        """Phase 3 (monitor/check) and Phase 4 (collect) belong to collect mode."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Phase 3" in workflow and "Phase 4" in workflow

    @pytest.mark.parametrize("keyword", EXPECTED_PHASE_KEYWORDS)
    def test_workflow_contains_keyword(self, skill_text, keyword):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert keyword in workflow, \
            f"Workflow missing content containing '{keyword}'"

    def test_phase1_writes_code(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "代码" in workflow or "code" in workflow.lower() or "脚本" in workflow

    def test_phase1_sanity_check(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "sanity" in workflow.lower() or "Sanity" in workflow

    def test_phase2_local_deployment(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "local" in workflow.lower() or "Local" in workflow

    def test_phase2_remote_deployment(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "remote" in workflow.lower() or "Remote" in workflow or "SSH" in workflow

    def test_phase3_detects_nan(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "NaN" in workflow or "nan" in workflow

    def test_phase3_detects_oom(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "OOM" in workflow or "out of memory" in workflow.lower()

    def test_phase3_auto_fix(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "自动修复" in workflow or "auto" in workflow.lower()

    def test_phase4_parses_results(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "解析" in workflow or "parse" in workflow.lower()

    def test_phase4_updates_status(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "completed" in workflow

    def test_phase4_sets_outcome(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        for outcome in ["succeeded", "failed", "inconclusive"]:
            assert outcome in workflow, f"Phase 4 must handle outcome: {outcome}"


# ── 4. Three run modes ────────────────────────────────────────────────

class TestRunModes:
    """Validate deploy / collect / full three-mode design."""

    def test_deploy_mode_is_default(self, skill_text):
        """Deploy mode is default (for planned experiments)."""
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "planned" in inputs, "Inputs must document that deploy mode requires status=planned"

    def test_collect_mode_documented(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "--collect" in inputs, "--collect mode must be documented in Inputs"

    def test_full_mode_documented(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "--full" in inputs, "--full mode must be documented in Inputs"

    def test_check_alias_mentioned(self, skill_text):
        """--check is a backward-compatible alias for --collect."""
        assert "--check" in skill_text, "--check alias must be mentioned (backward compat)"

    def test_deploy_returns_immediately(self, skill_text):
        """Deploy mode returns after Phase 1+2 without waiting for experiment."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert ("立即返回" in workflow or "immediately" in workflow.lower() or
                "返回" in workflow or "return" in workflow.lower()), \
            "Deploy mode must document that it returns immediately after launch"

    def test_collect_checks_if_alive_first(self, skill_text):
        """Collect mode must check if experiment is still running before collecting."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "alive" in workflow or "还在运行" in workflow or "仍在运行" in workflow, \
            "Collect mode must check alive status before collecting results"

    def test_collect_mode_requires_running_status(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "running" in inputs, "Collect mode requires status=running"

    def test_full_mode_runs_all_phases(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Full" in workflow or "--full" in workflow, \
            "Workflow must have a Full mode section"


# ── 5. Deploy report ───────────────────────────────────────────────────

class TestDeployReport:
    """Validate DEPLOY_REPORT is documented for deploy mode."""

    def test_deploy_report_mentioned(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "DEPLOY_REPORT" in workflow, "Deploy mode must output a DEPLOY_REPORT"

    def test_deploy_report_has_session_info(self, skill_text):
        assert "Session" in skill_text or "session" in skill_text, \
            "DEPLOY_REPORT must include session name info"

    def test_deploy_report_has_log_path(self, skill_text):
        assert "Log" in skill_text or "log" in skill_text, \
            "DEPLOY_REPORT must include log file path"

    def test_deploy_report_suggests_exp_status(self, skill_text):
        assert "/exp-status" in skill_text, \
            "DEPLOY_REPORT next steps must suggest /exp-status for monitoring"

    def test_deploy_saves_started_and_eta(self, skill_text):
        """Phase 2 must save started timestamp and estimated_hours to frontmatter."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "estimated_hours" in workflow, \
            "Phase 2 must write estimated_hours to experiment frontmatter"
        assert "started" in workflow, \
            "Phase 2 must write started timestamp to experiment frontmatter"

    def test_deploy_report_has_absolute_eta(self, skill_text):
        """DEPLOY_REPORT must show estimated completion as absolute timestamp."""
        assert "预计完成于" in skill_text or "estimated_hours" in skill_text, \
            "DEPLOY_REPORT must show absolute estimated completion time"


# ── 6. Experiment code location ────────────────────────────────────────

class TestExperimentCodeLocation:
    """Validate experiment code is written to standardized location."""

    def test_code_dir_in_wiki_writes(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "experiments/code/" in writes, \
            "Wiki Writes must document experiments/code/{slug}/ as code output location"

    def test_code_structure_documented(self, skill_text):
        """Must document the files written: train.py, config.yaml, run.sh."""
        assert "train.py" in skill_text, "Must document train.py in code structure"
        assert "config.yaml" in skill_text, "Must document config.yaml in code structure"
        assert "run.sh" in skill_text, "Must document run.sh in code structure"

    def test_code_not_in_project_root(self, skill_text):
        """Code should not be written to project root."""
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "experiments/code/" in constraints, \
            "Constraints must specify experiments/code/{slug}/ as the code location"


# ── 7. Environment support ──────────────────────────────────────────────

class TestEnvironment:
    """Validate local/remote deployment support."""

    def test_env_flag_documented(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "--env" in inputs

    def test_local_env(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "local" in inputs

    def test_remote_env(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "remote" in inputs


# ── 8. Experiment status transitions ─────────────────────────────────────

class TestStatusTransitions:
    """Validate experiment status lifecycle."""

    def test_planned_to_running(self, skill_text):
        assert "planned" in skill_text and "running" in skill_text

    def test_running_to_completed(self, skill_text):
        assert "running" in skill_text and "completed" in skill_text

    def test_rejects_completed_experiments(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "completed" in constraints or "abandoned" in constraints


# ── 9. Tool references ──────────────────────────────────────────────────

class TestToolReferences:
    """Validate all referenced tools exist."""

    def test_research_wiki_log_referenced(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "research_wiki.py" in deps

    def test_research_wiki_tool_exists(self):
        assert (TOOLS_DIR / "research_wiki.py").exists()

    def test_nvidia_smi_referenced(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "nvidia-smi" in deps

    def test_screen_referenced(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "screen" in deps


# ── 10. Review LLM integration ────────────────────────────────────────────────

class TestLLMReviewIntegration:
    """Validate Review LLM MCP server integration for optional code review."""

    def test_llm_review_chat_referenced(self, skill_text):
        assert "mcp__llm-review__chat" in skill_text

    def test_review_is_optional(self, skill_text):
        assert "--review" in skill_text

    def test_code_review_focus(self, skill_text):
        """Review LLM review should focus on code correctness."""
        assert "correctness" in skill_text.lower() or "正确性" in skill_text or \
               "training loop" in skill_text.lower()


# ── 11. Constraints ──────────────────────────────────────────────────────

class TestConstraints:
    """Validate constraints cover key rules."""

    def test_only_planned_or_running(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "planned" in constraints or "running" in constraints

    def test_collect_alive_no_wiki_write(self, skill_text):
        """When experiment is still alive in collect mode, wiki must not be written."""
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "alive" in constraints or "collect" in constraints.lower(), \
            "Constraints must cover collect-mode behavior when experiment still running"

    def test_sanity_must_pass(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "sanity" in constraints.lower()

    def test_results_saved_as_json(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "JSON" in constraints or "json" in constraints

    def test_multi_seed_mean_std(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "mean" in constraints.lower() or "均值" in constraints or "std" in constraints.lower()

    def test_auto_fix_limited(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "1" in constraints and ("次" in constraints or "attempt" in constraints.lower() or "尝试" in constraints)


# ── 12. Error handling ───────────────────────────────────────────────────

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_experiment_not_found(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "找不到" in errors or "not found" in errors.lower()

    def test_experiment_already_completed(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "已完成" in errors or "already" in errors.lower() or "completed" in errors

    def test_deploy_on_running_experiment(self, skill_text):
        """Deploy mode called on a running experiment should redirect to --collect."""
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "--collect" in errors or "collect" in errors.lower(), \
            "Error handling must redirect deploy-on-running to --collect mode"

    def test_gpu_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "GPU" in errors and ("不可用" in errors or "unavailable" in errors.lower())

    def test_review_llm_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "Review LLM" in errors or "review llm" in errors.lower() or "llm-review" in errors

    def test_sanity_check_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "sanity" in errors.lower()

    def test_remote_connection_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "SSH" in errors or "远程" in errors or "remote" in errors.lower()

    def test_partial_seed_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "seed" in errors.lower()


# ── 13. CLAUDE.md consistency ────────────────────────────────────────────

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_skill_listed_in_claude_md(self, claude_md_text):
        assert "exp-run" in claude_md_text, \
            "/exp-run must be listed in product CLAUDE.md skills table"

    def test_experiment_status_values(self, skill_text):
        """Status values must match CLAUDE.md experiment template."""
        for status in ["planned", "running", "completed", "abandoned"]:
            assert status in skill_text, \
                f"Experiment status '{status}' must be referenced"

    def test_outcome_values(self, skill_text):
        """Outcome values must match CLAUDE.md experiment template."""
        for outcome in ["succeeded", "failed", "inconclusive"]:
            assert outcome in skill_text, \
                f"Outcome value '{outcome}' must be referenced"

    def test_suggests_result_to_claim(self, skill_text):
        """Should suggest /exp-eval as next step."""
        assert "/exp-eval" in skill_text


# ── 14. Output report ──────────────────────────────────────────────────

class TestOutputReport:
    """Validate the run report format."""

    def test_report_includes_status(self, skill_text):
        assert "Status" in skill_text or "status" in skill_text

    def test_report_includes_results_table(self, skill_text):
        assert "Metric" in skill_text or "metric" in skill_text.lower()

    def test_report_includes_outcome(self, skill_text):
        assert "Outcome" in skill_text or "outcome" in skill_text

    def test_report_includes_next_steps(self, skill_text):
        assert "Next Steps" in skill_text or "next step" in skill_text.lower()


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

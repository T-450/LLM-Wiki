"""Tests for /exp-status SKILL.md structural completeness.

Validates that the exp-status skill follows extending.md structure,
supports four operating modes (default / --pipeline / --collect-ready /
--auto-advance), outputs a status table with alive/anomaly/completed
categories, and correctly integrates CronDelete + /research auto-advance.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "exp-status" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"exp-status SKILL.md not found at {SKILL_PATH}"
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
        assert re.search(r"^# /exp-status", skill_text, re.MULTILINE), \
            "SKILL.md must have '# /exp-status' heading"

    def test_has_intro_paragraph(self, skill_text):
        assert re.search(r"^>", skill_text, re.MULTILINE), \
            "SKILL.md must have intro paragraph (blockquote)"

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"


# ── 2. Input modes ────────────────────────────────────────────────────

class TestInputModes:
    """Validate all four operating modes are documented."""

    def test_no_args_mode_documented(self, skill_text):
        """Default (no args) mode: scan all running experiments."""
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "無参数" in inputs or "无参数" in inputs or \
               "default" in inputs.lower() or "No arguments" in inputs or \
               "不带参数" in inputs or "无参" in inputs or \
               "（默认）" in inputs or "(默认)" in inputs, \
            "Inputs must document the no-argument default mode"

    def test_pipeline_flag_documented(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "--pipeline" in inputs, "--pipeline flag must be documented"

    def test_collect_ready_flag_documented(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "--collect-ready" in inputs, "--collect-ready flag must be documented"

    def test_auto_advance_flag_documented(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "--auto-advance" in inputs, "--auto-advance flag must be documented"

    def test_auto_advance_requires_pipeline(self, skill_text):
        """--auto-advance must require --pipeline to work."""
        inputs = _extract_section(skill_text, "Inputs", level=2)
        # The inputs or constraints section should mention this dependency
        constraints = _extract_section(skill_text, "Constraints", level=2)
        combined = inputs + constraints
        assert "--pipeline" in combined and "--auto-advance" in combined, \
            "--auto-advance dependency on --pipeline must be documented"


# ── 3. Wiki interaction ────────────────────────────────────────────────

class TestWikiInteraction:
    """Validate wiki read/write documentation."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE)

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE)

    def test_has_graph_edges_subsection(self, skill_text):
        assert re.search(r"^###\s+Graph edges", skill_text, re.MULTILINE)

    def test_reads_experiments(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "experiments/" in reads

    def test_reads_pipeline_progress(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "pipeline-progress" in reads

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    def test_no_graph_edges_created(self, skill_text):
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert "无" in graph or "none" in graph.lower() or "不" in graph


# ── 4. Status table output ────────────────────────────────────────────

class TestStatusTable:
    """Validate status table includes all three experiment states."""

    def test_running_state_documented(self, skill_text):
        """Must show alive/running experiments."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "alive" in workflow or "running" in workflow.lower() or "运行" in workflow

    def test_anomaly_state_documented(self, skill_text):
        """Must detect and show anomaly state (NaN, OOM, etc.)."""
        assert "anomaly" in skill_text.lower() or "异常" in skill_text or \
               "NaN" in skill_text or "OOM" in skill_text

    def test_completed_pending_collect_state_documented(self, skill_text):
        """Must show 'session gone' / completed-but-not-collected state."""
        assert "session gone" in skill_text or \
               "pending collect" in skill_text.lower() or \
               "待收集" in skill_text or \
               "completed_pending_collect" in skill_text

    def test_output_has_actions_section(self, skill_text):
        """Status report must include suggested next actions."""
        assert "Actions" in skill_text or "操作" in skill_text or \
               "下一步" in skill_text


# ── 5. --auto-advance behavior ─────────────────────────────────────────

class TestAutoAdvance:
    """Validate --auto-advance correctly handles pipeline progression."""

    def test_advances_to_stage4(self, skill_text):
        """Must trigger /research --start-from stage4 when pipeline complete."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "stage4" in workflow or "Stage 4" in workflow, \
            "--auto-advance must trigger stage4 when complete"

    def test_does_not_advance_if_still_running(self, skill_text):
        """Must NOT advance if experiments are still running."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "尚未" in workflow or "not all" in workflow.lower() or \
               "仍有" in workflow or "still" in workflow.lower() or \
               "未完成" in workflow, \
            "Must document that --auto-advance does not advance when experiments still running"

    def test_pipeline_slug_from_progress_file(self, skill_text):
        """Pipeline slug must be read from pipeline-progress.md."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "pipeline-progress" in workflow

    def test_triggers_research_skill(self, skill_text):
        """Must call /research as sub-skill."""
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "/research" in deps or "research" in deps.lower()


# ── 6. --collect-ready behavior ───────────────────────────────────────

class TestCollectReady:
    """Validate --collect-ready auto-collects completed experiments."""

    def test_calls_exp_run_collect(self, skill_text):
        """--collect-ready must call /exp-run --collect for each completed experiment."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "--collect" in workflow or "collect" in workflow.lower()

    def test_calls_exp_run_skill(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "/exp-run" in deps


# ── 7. Tool references ────────────────────────────────────────────────

class TestToolReferences:
    """Validate all referenced tools exist."""

    def test_remote_check_referenced(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "remote.py" in deps or "remote" in deps

    def test_research_wiki_log_referenced(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "research_wiki.py" in deps

    def test_research_wiki_set_meta_referenced(self, skill_text):
        """set-meta is used to update pipeline-progress fields."""
        assert "set-meta" in skill_text or "set_meta" in skill_text

    def test_screen_referenced(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "screen" in deps

    def test_remote_py_exists(self):
        assert (TOOLS_DIR / "remote.py").exists()

    def test_research_wiki_py_exists(self):
        assert (TOOLS_DIR / "research_wiki.py").exists()


# ── 8. Constraints ────────────────────────────────────────────────────

class TestConstraints:
    """Validate key constraints are documented."""

    def test_no_wiki_write_in_default_mode(self, skill_text):
        """Default mode (no --collect-ready) should not modify wiki."""
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "只读" in constraints or "read" in constraints.lower() or \
               "不修改" in constraints or "collect-ready" in constraints, \
            "Must document read-only constraint for default mode"

    def test_auto_advance_requires_pipeline_constraint(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "--pipeline" in constraints and "--auto-advance" in constraints

    def test_auto_advance_requires_pipeline_flag(self, skill_text):
        """--auto-advance must require --pipeline to identify which pipeline to advance."""
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "--pipeline" in constraints and "--auto-advance" in constraints

    def test_anomaly_not_auto_fixed(self, skill_text):
        """exp-status only reports anomalies, does not fix them."""
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "修复" in constraints or "fix" in constraints.lower() or \
               "anomaly" in constraints.lower() or "异常" in constraints


# ── 9. Error handling ─────────────────────────────────────────────────

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_no_running_experiments(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "no running" in errors.lower() or "无运行中" in errors or \
               "没有" in errors or "找不到" in errors or \
               "No running" in errors

    def test_pipeline_progress_not_found(self, skill_text):
        """--pipeline mode must handle missing pipeline-progress.md."""
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "pipeline-progress" in errors or "progress" in errors.lower()

    def test_auto_advance_without_pipeline(self, skill_text):
        """--auto-advance without --pipeline should error gracefully."""
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "--pipeline" in errors or "--auto-advance" in errors

    def test_ssh_failure_degrades_gracefully(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "SSH" in errors or "连接失败" in errors or \
               "connection" in errors.lower()

    def test_collect_failure_continues(self, skill_text):
        """collect-ready failure on one experiment should not block others."""
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "collect" in errors.lower() or "--collect-ready" in errors


# ── 10. CLAUDE.md consistency ─────────────────────────────────────────

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_skill_listed_in_claude_md(self, claude_md_text):
        assert "exp-status" in claude_md_text, \
            "/exp-status must be listed in product CLAUDE.md skills table"

    def test_exp_status_flags_mentioned_in_claude_md(self, claude_md_text):
        """CLAUDE.md skills table should document exp-status flags."""
        lines = [l for l in claude_md_text.splitlines() if "exp-status" in l]
        assert any("pipeline" in l.lower() or "collect" in l.lower() or "auto" in l.lower()
                   for l in lines), \
            "CLAUDE.md skills table should document exp-status flags"

    def test_uses_wikilink_syntax(self, skill_text):
        assert "[[" in skill_text, "Must use wikilink syntax [[slug]] for wiki references"

    def test_experiment_status_values_referenced(self, skill_text):
        """Must reference valid experiment status values."""
        for status in ["running", "completed"]:
            assert status in skill_text, f"Must reference experiment status '{status}'"


# ── Helpers ────────────────────────────────────────────────────────────

def _extract_section(text: str, heading: str, level: int = 2) -> str:
    """Extract content under a markdown heading until the next same-level heading."""
    prefix = "#" * level
    pattern = rf"^{prefix}\s+{re.escape(heading)}.*?\n(.*?)(?=^{'#' * level}\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)
    # Fallback: partial heading match
    pattern = rf"^{prefix}\s+.*{re.escape(heading)}.*?\n(.*?)(?=^{'#' * level}\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""

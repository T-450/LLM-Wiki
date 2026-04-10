"""Tests for .claude/skills/research/SKILL.md"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "research" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
SKILLS_DIR = PROJECT_ROOT / ".claude" / "skills"


def _section_between(text: str, start_heading: str, end_heading: str) -> str:
    """Extract text between two markdown heading patterns (case-insensitive).

    Uses heading markers (### or ##) to find actual section headings,
    avoiding matches in body text.
    """
    start_pat = re.compile(r"^#{2,3}\s+" + re.escape(start_heading), re.MULTILINE | re.IGNORECASE)
    end_pat = re.compile(r"^#{2,3}\s+" + re.escape(end_heading), re.MULTILINE | re.IGNORECASE)
    m_start = start_pat.search(text)
    if not m_start:
        return ""
    rest = text[m_start.end():]
    m_end = end_pat.search(rest)
    if not m_end:
        return rest
    return rest[:m_end.start()]


def _workflow_section(text: str, heading: str) -> str:
    """Extract a workflow sub-section by its ### heading prefix.

    E.g. heading='Stage 1' matches '### Stage 1: Idea Discovery'.
    Returns text until the next ### heading.
    """
    pat = re.compile(r"^###\s+" + re.escape(heading) + r"[^\n]*\n", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return ""
    rest = text[m.end():]
    next_heading = re.search(r"^###\s+", rest, re.MULTILINE)
    if next_heading:
        return rest[:next_heading.start()]
    # Try ## heading
    next_h2 = re.search(r"^##\s+", rest, re.MULTILINE)
    if next_h2:
        return rest[:next_h2.start()]
    return rest


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"SKILL.md not found at {SKILL_PATH}"
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_md_text():
    assert CLAUDE_MD.exists(), f"CLAUDE.md not found at {CLAUDE_MD}"
    return CLAUDE_MD.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# TestSkillStructure (~9)
# ---------------------------------------------------------------------------
class TestSkillStructure:
    """Basic SKILL.md structural validation."""

    def test_file_exists(self):
        assert SKILL_PATH.exists()

    def test_has_yaml_frontmatter(self, skill_text):
        assert skill_text.startswith("---"), "Must begin with YAML frontmatter delimiter"
        parts = skill_text.split("---", 2)
        assert len(parts) >= 3, "Must have opening and closing --- delimiters"

    def test_frontmatter_has_description(self, skill_text):
        fm = skill_text.split("---", 2)[1]
        assert "description:" in fm

    def test_frontmatter_has_argument_hint(self, skill_text):
        fm = skill_text.split("---", 2)[1]
        assert "argument-hint:" in fm

    def test_heading_research_pipeline(self, skill_text):
        assert "# /research" in skill_text

    def test_intro_blockquote(self, skill_text):
        after_heading = skill_text.split("# /research", 1)[1]
        lines = [l.strip() for l in after_heading.strip().splitlines() if l.strip()]
        assert lines[0].startswith(">"), "First non-empty line after heading must be a blockquote"

    @pytest.mark.parametrize("section", [
        "## Inputs",
        "## Outputs",
        "## Wiki Interaction",
        "## Workflow",
        "## Constraints",
        "## Error Handling",
        "## Dependencies",
    ])
    def test_required_sections(self, skill_text, section):
        assert section in skill_text, f"Missing required section: {section}"


# ---------------------------------------------------------------------------
# TestWikiInteraction (~10)
# ---------------------------------------------------------------------------
class TestWikiInteraction:
    """Wiki Interaction section: Reads, Writes, Graph."""

    def test_reads_subsection_exists(self, skill_text):
        assert "### Reads" in skill_text

    def test_writes_subsection_exists(self, skill_text):
        assert "### Writes" in skill_text

    def test_graph_subsection_exists(self, skill_text):
        assert re.search(r"###\s+Graph", skill_text)

    def test_reads_ideas(self, skill_text):
        reads = _workflow_section(skill_text, "Reads")
        assert "wiki/ideas/" in reads

    def test_reads_experiments(self, skill_text):
        reads = _workflow_section(skill_text, "Reads")
        assert "wiki/experiments/" in reads

    def test_reads_claims(self, skill_text):
        reads = _workflow_section(skill_text, "Reads")
        assert "wiki/claims/" in reads

    def test_reads_context_brief(self, skill_text):
        reads = _workflow_section(skill_text, "Reads")
        assert "context_brief" in reads

    def test_reads_open_questions(self, skill_text):
        reads = _workflow_section(skill_text, "Reads")
        assert "open_questions" in reads

    def test_reads_pipeline_progress(self, skill_text):
        reads = _workflow_section(skill_text, "Reads")
        assert "pipeline-progress" in reads

    def test_writes_pipeline_progress(self, skill_text):
        writes = _workflow_section(skill_text, "Writes")
        assert "pipeline-progress" in writes

    def test_writes_log_md(self, skill_text):
        writes = _workflow_section(skill_text, "Writes")
        assert "log.md" in writes

    def test_no_direct_graph_edges(self, skill_text):
        graph_section = _workflow_section(skill_text, "Graph")
        assert re.search(r"(无|none|no)", graph_section, re.IGNORECASE), \
            "Pipeline should not create graph edges directly"

    def test_does_not_write_wiki_entities_directly(self, skill_text):
        writes = _workflow_section(skill_text, "Writes")
        # Should mention delegation, not direct entity writing
        assert re.search(r"(委托|delegat)", writes, re.IGNORECASE), \
            "Writes section should note that wiki entity writes are delegated"


# ---------------------------------------------------------------------------
# TestWorkflow (~14)
# ---------------------------------------------------------------------------
class TestWorkflow:
    """Workflow section: Step 0, 5 Stages, 2 Gates, Final."""

    def test_step_0_init(self, skill_text):
        assert re.search(r"Step\s*0.*初始化|Step\s*0.*[Ii]nit", skill_text)

    def test_stage_1_exists(self, skill_text):
        assert re.search(r"Stage\s*1", skill_text)

    def test_stage_2_exists(self, skill_text):
        assert re.search(r"Stage\s*2", skill_text)

    def test_stage_3_exists(self, skill_text):
        assert re.search(r"Stage\s*3", skill_text)

    def test_stage_4_exists(self, skill_text):
        assert re.search(r"Stage\s*4", skill_text)

    def test_stage_5_exists(self, skill_text):
        assert re.search(r"Stage\s*5", skill_text)

    def test_gate_1_exists(self, skill_text):
        assert re.search(r"Gate\s*1", skill_text)

    def test_gate_2_exists(self, skill_text):
        assert re.search(r"Gate\s*2", skill_text)

    def test_step_final_report(self, skill_text):
        assert re.search(r"(Step\s+Final|Pipeline\s+Report)", skill_text)

    def test_stage_1_calls_idea_generation(self, skill_text):
        stage1 = _workflow_section(skill_text, "Stage 1")
        assert "/ideate" in stage1

    def test_gate_1_user_selects_idea(self, skill_text):
        gate1 = _workflow_section(skill_text, "Gate 1")
        assert re.search(r"(select|选择).*idea", gate1, re.IGNORECASE)

    def test_gate_1_auto_selects_top_1(self, skill_text):
        gate1 = _workflow_section(skill_text, "Gate 1")
        assert re.search(r"(top.?1|priority.*最高|highest.*priority)", gate1, re.IGNORECASE)

    def test_stage_2_calls_experiment_plan(self, skill_text):
        stage2 = _workflow_section(skill_text, "Stage 2")
        assert "/exp-design" in stage2

    def test_stage_2_uses_review_flag(self, skill_text):
        stage2 = _workflow_section(skill_text, "Stage 2")
        assert "--review" in stage2

    def test_stage_3_calls_run_experiment(self, skill_text):
        stage3 = _workflow_section(skill_text, "Stage 3")
        assert "/exp-run" in stage3

    def test_stage_4_calls_result_to_claim(self, skill_text):
        stage4 = _workflow_section(skill_text, "Stage 4")
        assert "/exp-eval" in stage4

    def test_stage_4_may_loop_with_refine(self, skill_text):
        stage4 = _workflow_section(skill_text, "Stage 4")
        assert "/refine" in stage4

    def test_stage_5_calls_paper_plan(self, skill_text):
        stage5 = _workflow_section(skill_text, "Stage 5")
        assert "/paper-plan" in stage5

    def test_stage_5_calls_paper_write(self, skill_text):
        stage5 = _workflow_section(skill_text, "Stage 5")
        assert "/paper-draft" in stage5

    def test_stage_5_calls_refine_loop(self, skill_text):
        stage5 = _workflow_section(skill_text, "Stage 5")
        assert "/refine" in stage5

    def test_stage_5_calls_paper_compile(self, skill_text):
        stage5 = _workflow_section(skill_text, "Stage 5")
        assert "/paper-compile" in stage5

    def test_final_report_output(self, skill_text):
        final_section = _workflow_section(skill_text, "Step Final")
        assert re.search(r"(report|报告|PIPELINE_REPORT)", final_section, re.IGNORECASE)


# ---------------------------------------------------------------------------
# TestSkillDelegation (~10)
# ---------------------------------------------------------------------------
class TestSkillDelegation:
    """Validates delegation to 8 other skills."""

    DELEGATED_SKILLS = [
        "ideate",
        "exp-design",
        "exp-run",
        "exp-status",
        "exp-eval",
        "refine",
        "paper-plan",
        "paper-draft",
        "paper-compile",
    ]

    @pytest.mark.parametrize("skill_name", DELEGATED_SKILLS)
    def test_references_delegated_skill(self, skill_text, skill_name):
        assert f"/{skill_name}" in skill_text, \
            f"Must reference /{skill_name} in the workflow"

    @pytest.mark.parametrize("skill_name", DELEGATED_SKILLS)
    def test_delegated_skill_exists_on_disk(self, skill_name):
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        assert skill_md.exists(), f"Delegated skill SKILL.md not found: {skill_md}"

    def test_uses_skill_tool_not_bash(self, skill_text):
        deps = _section_between(skill_text, "Dependencies", "NONEXISTENT_SECTION_SENTINEL")
        assert re.search(r"Skill\s*(tool|：|—|\(|（)", deps, re.IGNORECASE), \
            "Should reference Skill tool for delegation"

    def test_no_logic_embedding_constraint(self, skill_text):
        constraints = _section_between(skill_text, "Constraints", "Error Handling")
        assert re.search(r"(不嵌入|not.*embed|delegat|委托)", constraints, re.IGNORECASE), \
            "Constraints should prohibit embedding skill logic"


# ---------------------------------------------------------------------------
# TestParameters (~6)
# ---------------------------------------------------------------------------
class TestParameters:
    """CLI parameters: --auto, --start-from, --skip-paper, --venue."""

    def test_auto_mode_documented(self, skill_text):
        assert "--auto" in skill_text

    def test_start_from_documented(self, skill_text):
        assert "--start-from" in skill_text

    def test_start_from_stages_1_to_5(self, skill_text):
        inputs = _section_between(skill_text, "Inputs", "Outputs")
        assert re.search(r"--start-from.*[1-5]|stage.*1.*5", inputs, re.IGNORECASE)

    def test_start_from_has_stage3_collect(self, skill_text):
        """stage3-collect is a new valid --start-from value."""
        inputs = _section_between(skill_text, "Inputs", "Outputs")
        assert "stage3-collect" in inputs, \
            "--start-from must include stage3-collect for resuming at collect phase"

    def test_start_from_has_stage3_check(self, skill_text):
        """stage3-check is a new valid --start-from value."""
        assert "stage3-check" in skill_text, \
            "--start-from must include stage3-check for status-only resume"

    def test_skip_paper_documented(self, skill_text):
        assert "--skip-paper" in skill_text

    def test_venue_documented(self, skill_text):
        assert "--venue" in skill_text

    def test_auto_gate_1_selects_top_1(self, skill_text):
        gate1 = _workflow_section(skill_text, "Gate 1")
        assert re.search(r"(auto|--auto).*top.?1|top.?1.*auto|自动.*选择|自动.*priority", gate1, re.IGNORECASE)

    def test_auto_gate_2_continues(self, skill_text):
        gate2 = _workflow_section(skill_text, "Gate 2")
        assert re.search(r"(auto|--auto).*continu|auto.*自动.*继续|自动继续", gate2, re.IGNORECASE)

    def test_venue_passed_to_paper_plan(self, skill_text):
        stage5 = _workflow_section(skill_text, "Stage 5")
        assert re.search(r"/paper-plan.*--venue|--venue.*venue", stage5)


# ---------------------------------------------------------------------------
# TestGateSystem (~8)
# ---------------------------------------------------------------------------
class TestGateSystem:
    """Gate 1 and Gate 2 properties."""

    def test_gate_1_between_stage_1_and_2(self, skill_text):
        # Gate 1 heading should appear between Stage 1 and Stage 2 headings
        pat_s1 = re.search(r"^###\s+Stage 1", skill_text, re.MULTILINE)
        pat_g1 = re.search(r"^###\s+Gate 1", skill_text, re.MULTILINE)
        pat_s2 = re.search(r"^###\s+Stage 2", skill_text, re.MULTILINE)
        assert pat_s1 and pat_g1 and pat_s2
        assert pat_s1.start() < pat_g1.start() < pat_s2.start()

    def test_gate_2_between_stage_4_and_5(self, skill_text):
        pat_s4 = re.search(r"^###\s+Stage 4", skill_text, re.MULTILINE)
        pat_g2 = re.search(r"^###\s+Gate 2", skill_text, re.MULTILINE)
        pat_s5 = re.search(r"^###\s+Stage 5", skill_text, re.MULTILINE)
        assert pat_s4 and pat_g2 and pat_s5
        assert pat_s4.start() < pat_g2.start() < pat_s5.start()

    def test_gates_save_progress(self, skill_text):
        gate1 = _workflow_section(skill_text, "Gate 1")
        gate2 = _workflow_section(skill_text, "Gate 2")
        assert re.search(r"(保存|save|progress|进度)", gate1, re.IGNORECASE)
        assert re.search(r"(保存|save|progress|进度)", gate2, re.IGNORECASE)

    def test_progress_file_in_wiki_outputs(self, skill_text):
        assert "wiki/outputs/pipeline-progress" in skill_text

    def test_auto_skips_gate_interaction(self, skill_text):
        assert re.search(
            r"--auto.*跳过|auto.*skip.*interact|auto.*模式.*跳过|auto.*skip.*confirm|auto.*skips.*confirm",
            skill_text, re.IGNORECASE
        )

    def test_user_can_stop_at_gate(self, skill_text):
        gate1 = _workflow_section(skill_text, "Gate 1")
        assert re.search(r"stop|停止|pause", gate1, re.IGNORECASE)

    def test_resume_from_gate(self, skill_text):
        assert re.search(r"(恢复|resume|recover|--start-from)", skill_text, re.IGNORECASE)

    def test_ask_user_question_in_interactive(self, skill_text):
        assert "AskUserQuestion" in skill_text


# ---------------------------------------------------------------------------
# TestIterationControl (~5)
# ---------------------------------------------------------------------------
class TestIterationControl:
    """Iteration and loop bounds."""

    def test_stage_234_loop_max_2(self, skill_text):
        assert re.search(r"(最多.*2.*轮|max.*2.*iter|loop.*2|2.*轮|2.*iteration)", skill_text, re.IGNORECASE)

    def test_auto_retries_stage_1_max_once(self, skill_text):
        stage4 = _workflow_section(skill_text, "Stage 4")
        assert re.search(r"(最多.*1.*次|max.*1|一次|once)", stage4, re.IGNORECASE)

    def test_convergence_detection(self, skill_text):
        stage4 = _workflow_section(skill_text, "Stage 4")
        assert re.search(r"(supported|充分|sufficient|converge)", stage4, re.IGNORECASE)

    def test_primary_claim_confidence_threshold(self, skill_text):
        stage4 = _workflow_section(skill_text, "Stage 4")
        assert re.search(r"0\.7|70%", stage4)

    def test_claims_insufficient_triggers_loop(self, skill_text):
        stage4 = _workflow_section(skill_text, "Stage 4")
        assert re.search(r"(不足|insufficien|weakly|partial|回.*Stage\s*2|back.*Stage\s*2)",
                         stage4, re.IGNORECASE)


# ---------------------------------------------------------------------------
# TestProgressPersistence (~5)
# ---------------------------------------------------------------------------
class TestProgressPersistence:
    """Progress file management."""

    def test_progress_file_created_in_step_0(self, skill_text):
        step0 = _workflow_section(skill_text, "Step 0")
        assert re.search(r"(进度文件|progress.*file|pipeline-progress)", step0, re.IGNORECASE)

    def test_progress_file_updated_at_gates(self, skill_text):
        gate1 = _workflow_section(skill_text, "Gate 1")
        gate2 = _workflow_section(skill_text, "Gate 2")
        assert re.search(r"(进度|progress|update)", gate1, re.IGNORECASE)
        assert re.search(r"(进度|progress|update)", gate2, re.IGNORECASE)

    def test_progress_contains_idea_slug(self, skill_text):
        assert "idea_slug" in skill_text

    def test_progress_contains_experiment_slugs(self, skill_text):
        assert "experiment_slugs" in skill_text

    def test_progress_contains_claim_slugs(self, skill_text):
        assert "claim_slugs" in skill_text

    def test_status_tracking(self, skill_text):
        assert "status: running" in skill_text
        assert "status: completed" in skill_text

    def test_resume_from_progress_file(self, skill_text):
        step0 = _workflow_section(skill_text, "Step 0")
        assert re.search(r"(恢复|resume|recover|progress)", step0, re.IGNORECASE)


# ---------------------------------------------------------------------------
# TestConstraints (~8)
# ---------------------------------------------------------------------------
class TestConstraints:
    """Constraints section validation."""

    def _constraints(self, skill_text):
        return _section_between(skill_text, "Constraints", "Error Handling")

    def test_orchestration_only(self, skill_text):
        c = self._constraints(skill_text)
        assert re.search(r"(不嵌入|not.*embed|orchestrat|委托|delegat)", c, re.IGNORECASE)

    def test_gates_save_progress_constraint(self, skill_text):
        c = self._constraints(skill_text)
        assert re.search(r"(Gate.*保存|Gate.*save|Gate.*progress)", c, re.IGNORECASE)

    def test_max_iterations_documented(self, skill_text):
        c = self._constraints(skill_text)
        assert re.search(r"(最多|max).*[12].*(轮|iter|loop|次)", c, re.IGNORECASE)

    def test_no_direct_wiki_entity_writes(self, skill_text):
        c = self._constraints(skill_text)
        assert re.search(r"(不直接.*wiki|no.*direct.*wiki|不直接修改)", c, re.IGNORECASE)

    def test_skip_paper_still_does_stage_4(self, skill_text):
        c = self._constraints(skill_text)
        assert re.search(r"(--skip-paper.*exp-eval|--skip-paper.*Stage\s*4|skip-paper.*claim)",
                         c, re.IGNORECASE)

    def test_log_at_every_stage(self, skill_text):
        c = self._constraints(skill_text)
        assert re.search(r"(每个.*Stage.*log|log.*every|Stage.*追加.*log|Stage.*log|log.*审计)",
                         c, re.IGNORECASE)

    def test_progress_file_format(self, skill_text):
        c = self._constraints(skill_text)
        assert re.search(r"(进度文件.*wiki/outputs|progress.*wiki/outputs|pipeline-progress)",
                         c, re.IGNORECASE)

    def test_skill_tool_for_delegation(self, skill_text):
        c = self._constraints(skill_text)
        assert re.search(r"(Skill.*tool|Skill.*委托|via.*Skill)", c, re.IGNORECASE)


# ---------------------------------------------------------------------------
# TestErrorHandling (~6)
# ---------------------------------------------------------------------------
class TestErrorHandling:
    """Error Handling section validation."""

    def _errors(self, skill_text):
        return _section_between(skill_text, "Error Handling", "Dependencies")

    def test_delegated_skill_failure(self, skill_text):
        e = self._errors(skill_text)
        assert re.search(r"(skill.*fail|失败|委托.*fail)", e, re.IGNORECASE)

    def test_all_ideas_failed(self, skill_text):
        e = self._errors(skill_text)
        assert re.search(r"(all.*idea.*fail|ideas.*失败|idea.*无)", e, re.IGNORECASE)

    def test_all_experiments_failed(self, skill_text):
        e = self._errors(skill_text)
        assert re.search(r"(all.*experiment.*fail|实验.*失败|实验.*全失败)", e, re.IGNORECASE)

    def test_gate_stop_saves_progress(self, skill_text):
        e = self._errors(skill_text)
        assert re.search(r"(stop.*save|停止.*保存|save.*progress|保存.*进度)", e, re.IGNORECASE)

    def test_progress_file_corruption_recovery(self, skill_text):
        e = self._errors(skill_text)
        assert re.search(r"(corrupt|损坏|推断|infer|recover)", e, re.IGNORECASE)

    def test_wiki_empty(self, skill_text):
        e = self._errors(skill_text)
        assert re.search(r"(wiki.*空|wiki.*empty|空.*wiki)", e, re.IGNORECASE)


# ---------------------------------------------------------------------------
# TestToolReferences (~5)
# ---------------------------------------------------------------------------
class TestToolReferences:
    """Tool and native capability references."""

    def test_uses_research_wiki_slug(self, skill_text):
        assert re.search(r"research_wiki\.py\s+slug", skill_text)

    def test_uses_research_wiki_log(self, skill_text):
        assert re.search(r"research_wiki\.py\s+log", skill_text)

    @pytest.mark.parametrize("tool", ["Skill", "Read", "Write", "Glob", "AskUserQuestion"])
    def test_native_tool_referenced(self, skill_text, tool):
        assert tool in skill_text, f"Must reference native tool: {tool}"

    def test_no_direct_mcp_servers(self, skill_text):
        deps = _section_between(skill_text, "Dependencies", "NONEXISTENT_SECTION_SENTINEL")
        assert re.search(r"(无直接|no.*direct|none)", deps, re.IGNORECASE)


# ---------------------------------------------------------------------------
# TestClaudeMdConsistency (~4)
# ---------------------------------------------------------------------------
class TestClaudeMdConsistency:
    """Cross-check with product CLAUDE.md."""

    def test_log_md_format_in_claude_md(self, claude_md_text):
        assert "log.md" in claude_md_text
        assert "append-only" in claude_md_text

    def test_outputs_dir_in_claude_md(self, claude_md_text):
        assert "outputs/" in claude_md_text

    def test_pipeline_progress_format_consistent(self, skill_text):
        # Progress file uses YAML frontmatter
        assert "pipeline-progress" in skill_text
        assert "slug:" in skill_text
        assert "status:" in skill_text

    def test_log_format_consistent(self, skill_text, claude_md_text):
        # CLAUDE.md log format: ## [DATE] skill | action | details
        assert "research |" in skill_text
        # CLAUDE.md mentions log format
        assert re.search(r"log\.md.*format|log\.md.*append", claude_md_text, re.IGNORECASE)


# ---------------------------------------------------------------------------
# TestPipelineReport (~5)
# ---------------------------------------------------------------------------
class TestPipelineReport:
    """Final pipeline report structure."""

    def _report(self, skill_text):
        idx = skill_text.find("Step Final")
        if idx == -1:
            idx = skill_text.find("Pipeline Report")
        return skill_text[idx:] if idx != -1 else ""

    def test_report_has_stage_summary(self, skill_text):
        report = self._report(skill_text)
        assert re.search(r"Stage\s+Summary|Stage.*Status", report, re.IGNORECASE)

    def test_report_has_claims_trail(self, skill_text):
        report = self._report(skill_text)
        assert re.search(r"Claims?\s+Trail|Initial.*Final|proposed.*supported", report, re.IGNORECASE)

    def test_report_has_iteration_history(self, skill_text):
        report = self._report(skill_text)
        assert re.search(r"Iteration\s+History|iteration|loop.*iteration", report, re.IGNORECASE)

    def test_report_has_deliverables(self, skill_text):
        report = self._report(skill_text)
        assert re.search(r"Deliverable", report, re.IGNORECASE)

    def test_report_has_next_steps(self, skill_text):
        report = self._report(skill_text)
        assert re.search(r"Next\s+Steps", report, re.IGNORECASE)


# ---------------------------------------------------------------------------
# TestStage3Redesign (~6) — non-blocking async experiment execution
# ---------------------------------------------------------------------------
class TestStage3Redesign:
    """Stage 3 is non-blocking: deploy(3a) → await(3b) → collect(3c)."""

    def test_stage3_has_three_substages(self, skill_text):
        """Stage 3 must be split into 3a (deploy), 3b (await), 3c (collect)."""
        assert re.search(r"Stage\s*3a", skill_text, re.IGNORECASE), \
            "Stage 3a (Deploy All) must be documented"
        assert re.search(r"Stage\s*3b", skill_text, re.IGNORECASE), \
            "Stage 3b (Await) must be documented"
        assert re.search(r"Stage\s*3c", skill_text, re.IGNORECASE), \
            "Stage 3c (Collect) must be documented"

    def test_stage3a_uses_deploy_mode(self, skill_text):
        """Stage 3a must call /exp-run in deploy mode (NOT --full)."""
        stage3 = _section_between(skill_text, "Stage 3", "Stage 4")
        # Should NOT use --full (which would block); default deploy mode is correct
        assert "/exp-run" in stage3, "Stage 3a must call /exp-run"
        assert "--full" not in stage3, \
            "Stage 3a must use default deploy mode, not --full (which blocks)"

    def test_stage3b_prints_instructions_and_exits(self, skill_text):
        """Stage 3b must print clear instructions for user to resume after experiments finish."""
        stage3 = _section_between(skill_text, "Stage 3", "Stage 4")
        assert "stage3-collect" in stage3, \
            "Stage 3b must tell user to run --start-from stage3-collect when experiments finish"

    def test_stage3b_shows_eta(self, skill_text):
        """Stage 3b must show estimated completion time for each experiment."""
        stage3 = _section_between(skill_text, "Stage 3", "Stage 4")
        assert "estimated_hours" in stage3 or "预计完成" in stage3 or "eta" in stage3.lower(), \
            "Stage 3b must compute and display ETA for each deployed experiment"

    def test_stage3b_recommends_return_time(self, skill_text):
        """Stage 3b must tell user when to come back (recommended return time)."""
        stage3 = _section_between(skill_text, "Stage 3", "Stage 4")
        assert "建议" in stage3 or "recommend" in stage3.lower() or "之后运行" in stage3, \
            "Stage 3b must suggest a specific time for user to return"

    def test_stage3b_session_ends_after_deploy(self, skill_text):
        """Stage 3b must document that the current session can close after deploy."""
        stage3 = _section_between(skill_text, "Stage 3", "Stage 4")
        assert re.search(r"(session.*关闭|session.*close|可以关闭|结束.*session)",
                         stage3, re.IGNORECASE), \
            "Stage 3b must indicate current session can be closed after deploy"

    def test_stage3c_triggered_by_start_from(self, skill_text):
        """stage3-collect must be a valid --start-from value."""
        inputs = _section_between(skill_text, "Inputs", "Outputs")
        assert "stage3-collect" in inputs or "stage3-collect" in skill_text, \
            "stage3-collect must be a valid --start-from value"

    def test_stage3c_uses_collect_mode(self, skill_text):
        """Stage 3c must call /exp-run --collect, not the full mode."""
        stage3 = _section_between(skill_text, "Stage 3", "Stage 4")
        assert "--collect" in stage3, \
            "Stage 3c must call /exp-run --collect for result collection"


# ---------------------------------------------------------------------------
# TestAutoRecovery (~4) — detect unfinished pipeline on new invocation
# ---------------------------------------------------------------------------
class TestAutoRecovery:
    """When /research is called without --start-from and pipeline-progress exists."""

    def test_detects_running_pipeline(self, skill_text):
        """Step 0 must check pipeline-progress.md for unfinished pipelines."""
        step0 = _workflow_section(skill_text, "Step 0")
        assert re.search(r"(自动恢复|auto.?recover|未完成|running.*pipeline|pipeline.*running)",
                         step0, re.IGNORECASE), \
            "Step 0 must detect unfinished pipeline in pipeline-progress.md"

    def test_prompts_user_on_recovery(self, skill_text):
        """Must prompt user to choose: continue / new / check status."""
        step0 = _workflow_section(skill_text, "Step 0")
        assert re.search(r"(继续|continue|continue.*[1]|从.*继续)", step0, re.IGNORECASE), \
            "Must offer option to continue from current stage"
        assert re.search(r"(新的|new.*pipeline|开始新|[2].*new)", step0, re.IGNORECASE), \
            "Must offer option to start new pipeline"

    def test_auto_mode_auto_continues(self, skill_text):
        """In --auto mode, auto-recovery should automatically continue (no prompt)."""
        step0 = _workflow_section(skill_text, "Step 0")
        assert re.search(r"(--auto.*继续|auto.*自动.*[1]|--auto.*continue|auto.*选.*1)",
                         step0, re.IGNORECASE), \
            "--auto mode must automatically choose to continue the unfinished pipeline"

    def test_new_pipeline_overwrites_progress(self, skill_text):
        """Choosing to start new pipeline must overwrite old pipeline-progress.md."""
        step0 = _workflow_section(skill_text, "Step 0")
        assert re.search(r"(覆盖|overwrite|覆盖.*旧|new.*pipeline.*overwrit|new.*覆盖)",
                         step0, re.IGNORECASE), \
            "Starting a new pipeline must document that old progress is overwritten"


# ---------------------------------------------------------------------------
# TestBootstrapStage0 — Seed & Grow cold-start solution
# ---------------------------------------------------------------------------
class TestBootstrapStage0:
    """Stage 0: Bootstrap auto-triggers when wiki is cold."""

    def test_stage_0_exists(self, skill_text):
        assert re.search(r"Stage\s*0.*Bootstrap", skill_text, re.IGNORECASE)

    def test_stage_0_trigger_condition(self, skill_text):
        stage0 = _workflow_section(skill_text, "Stage 0")
        assert re.search(r"maturity.*--json", stage0), \
            "Stage 0 must check maturity via research_wiki.py maturity"

    def test_stage_0_cold_trigger(self, skill_text):
        stage0 = _workflow_section(skill_text, "Stage 0")
        assert re.search(r'cold', stage0, re.IGNORECASE), \
            "Stage 0 must trigger on cold maturity level"

    def test_stage_0_auto_ingest(self, skill_text):
        stage0 = _workflow_section(skill_text, "Stage 0")
        assert re.search(r"(auto.*ingest|ingest|Skill.*ingest)", stage0, re.IGNORECASE), \
            "Stage 0 must auto-ingest papers via /ingest"

    def test_stage_0_search_sources(self, skill_text):
        stage0 = _workflow_section(skill_text, "Stage 0")
        assert re.search(r"(fetch_deepxiv|DeepXiv)", stage0), \
            "Stage 0 must search DeepXiv"
        assert re.search(r"(fetch_s2|Semantic Scholar|S2)", stage0), \
            "Stage 0 must search Semantic Scholar"

    def test_stage_0_bootstrap_report(self, skill_text):
        stage0 = _workflow_section(skill_text, "Stage 0")
        assert re.search(r"(Bootstrap.*完成|Bootstrap.*report|报告)", stage0, re.IGNORECASE), \
            "Stage 0 must output a bootstrap summary report"

    def test_stage_0_in_pipeline_progress(self, skill_text):
        assert re.search(r"Stage\s*0.*Bootstrap.*skipped", skill_text), \
            "Pipeline progress template must include Stage 0"

    def test_stage_0_in_stage_summary(self, skill_text):
        report = skill_text[skill_text.find("Step Final"):] if "Step Final" in skill_text else ""
        assert re.search(r"Stage\s*0.*Bootstrap", report, re.IGNORECASE), \
            "Pipeline report Stage Summary must include Stage 0"

    def test_error_handling_auto_bootstrap(self, skill_text):
        errors = _section_between(skill_text, "Error Handling", "Dependencies")
        assert re.search(r"(Stage 0|Bootstrap|auto.*ingest|自动)", errors, re.IGNORECASE), \
            "Error handling for empty wiki must reference auto-bootstrap"

    def test_maturity_tool_in_dependencies(self, skill_text):
        idx = skill_text.find("## Dependencies")
        deps = skill_text[idx:] if idx != -1 else ""
        assert re.search(r"maturity", deps), \
            "maturity tool must be listed in dependencies"


# ---------------------------------------------------------------------------
# TestWikiGrowthReport — Growth feedback in pipeline report
# ---------------------------------------------------------------------------
class TestWikiGrowthReport:
    """Pipeline report must include Wiki Growth section."""

    def test_growth_section_in_report(self, skill_text):
        report = skill_text[skill_text.find("Step Final"):] if "Step Final" in skill_text else ""
        assert re.search(r"Wiki\s+Growth", report, re.IGNORECASE), \
            "Pipeline report must include Wiki Growth section"

    def test_growth_has_maturity_comparison(self, skill_text):
        report = skill_text[skill_text.find("Step Final"):] if "Step Final" in skill_text else ""
        assert re.search(r"Maturity", report, re.IGNORECASE), \
            "Wiki Growth must show maturity level comparison"

    def test_maturity_snapshot_in_step_0(self, skill_text):
        step0 = _workflow_section(skill_text, "Step 0")
        assert re.search(r"(maturity.*before|maturity_before|Snapshot|snapshot)", step0, re.IGNORECASE), \
            "Step 0 must snapshot maturity for Growth Report comparison"

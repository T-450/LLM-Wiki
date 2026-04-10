"""Tests for /exp-design SKILL.md structural completeness.

Validates that the exp-design skill follows extending.md structure,
designs claim-driven experiments with ablation support, references correct
tools, documents wiki interactions, and aligns with product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "exp-design" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"exp-design SKILL.md not found at {SKILL_PATH}"
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
        assert re.search(r"^# /exp-design", skill_text, re.MULTILINE), \
            "SKILL.md must have '# /exp-design' heading"

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

    def test_reads_ideas(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "ideas/" in reads

    def test_reads_claims(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "claims/" in reads

    def test_reads_experiments(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "experiments/" in reads

    def test_reads_papers(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "papers/" in reads

    def test_reads_query_pack(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "context_brief.md" in reads

    def test_reads_gap_map(self, skill_text):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert "open_questions.md" in reads

    def test_writes_experiments(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "experiments/" in writes

    def test_writes_ideas(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "ideas/" in writes

    def test_writes_edges(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "edges.jsonl" in writes

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    def test_graph_edge_tested_by(self, skill_text):
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert "tested_by" in graph


# ── 3. Workflow — 6 steps ──────────────────────────────────────────────

EXPECTED_WORKFLOW_KEYWORDS = [
    ("上下文", "context"),          # Step 1: load context (en) / 上下文 (zh)
    ("界定", "scope"),              # Step 2: scope claims (en) / 界定 (zh)
    ("实验块", "experiment block"), # Step 3: design experiment blocks (en) / 实验块 (zh)
    ("执行顺序", "run order"),      # Step 4: build run order (en) / 执行顺序 (zh)
    ("Review LLM", "review llm"),    # Step 5: optional review
    ("写入 Wiki", "write to wiki"), # Step 6: write to wiki (en) / 写入 Wiki (zh)
]


class TestWorkflow:
    """Validate workflow covers all 6 required steps."""

    def test_has_at_least_6_steps(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        steps = re.findall(r"^### Step \d+", workflow, re.MULTILINE)
        assert len(steps) >= 6, f"Expected >= 6 workflow steps, found {len(steps)}"

    @pytest.mark.parametrize("zh_kw,en_kw", EXPECTED_WORKFLOW_KEYWORDS)
    def test_workflow_contains_keyword(self, skill_text, zh_kw, en_kw):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert zh_kw in workflow or en_kw in workflow.lower(), \
            f"Workflow missing content containing '{zh_kw}' or '{en_kw}'"

    def test_step1_loads_idea(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "idea" in workflow.lower() and ("slug" in workflow.lower() or "hypothesis" in workflow.lower())

    def test_step2_has_target_dimension(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "target" in workflow.lower()

    def test_step2_has_decomposition_dimension(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "decomposition" in workflow.lower()

    def test_step2_has_threats_dimension(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "threat" in workflow.lower()

    def test_step3_has_experiment_types(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        for exp_type in ["baseline", "validation", "ablation", "robustness"]:
            assert exp_type.lower() in workflow.lower() or \
                   exp_type.capitalize() in workflow, \
                f"Missing experiment type: {exp_type}"

    def test_step4_has_decision_gates(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "决策门" in workflow or "decision gate" in workflow.lower() or "门" in workflow

    def test_step4_has_stages(self, skill_text):
        """Run order should have at least sanity + anchor + main stages."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Stage" in workflow or "stage" in workflow

    def test_step5_llm_review(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "mcp__llm-review__chat" in workflow

    def test_step6_creates_experiment_pages(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "experiments/{slug}.md" in workflow or "experiments/" in workflow

    def test_step6_adds_graph_edges(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "add-edge" in workflow

    def test_step6_rebuilds_derived_data(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "rebuild-context-brief" in workflow
        assert "rebuild-open-questions" in workflow


# ── 4. Experiment block design ──────────────────────────────────────────

class TestExperimentBlocks:
    """Validate 4 experiment block types are documented."""

    @pytest.mark.parametrize("block_type", ["Baseline", "Validation", "Ablation", "Robustness"])
    def test_block_type_documented(self, skill_text, block_type):
        assert block_type in skill_text or block_type.lower() in skill_text.lower(), \
            f"Experiment block type '{block_type}' must be documented"

    def test_baseline_reproduces_prior_results(self, skill_text):
        assert "基线" in skill_text or "baseline" in skill_text.lower()

    def test_ablation_isolates_factors(self, skill_text):
        assert "因素" in skill_text or "factor" in skill_text.lower() or "隔离" in skill_text

    def test_robustness_tests_generality(self, skill_text):
        assert "鲁棒性" in skill_text or "robustness" in skill_text.lower() or "通用性" in skill_text

    def test_each_block_has_target_claim(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "target_claim" in workflow

    def test_each_block_has_success_criterion(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "success_criterion" in workflow or "success criterion" in workflow.lower()

    def test_each_block_has_gpu_hours(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "gpu" in workflow.lower() or "GPU" in workflow


# ── 5. Claims handling ──────────────────────────────────────────────────

class TestClaimsHandling:
    """Validate claims-driven design approach."""

    def test_target_claim_identified(self, skill_text):
        assert "target" in skill_text.lower()

    def test_decomposition_claims_identified(self, skill_text):
        assert "decomposition" in skill_text.lower()

    def test_new_claims_created_if_missing(self, skill_text):
        assert "创建" in skill_text or "create" in skill_text.lower()
        assert "proposed" in skill_text  # new claims have status: proposed

    def test_claims_scoped_not_modified(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "界定" in constraints or "scoped" in constraints.lower() or "不修改" in constraints


# ── 6. Tool references ──────────────────────────────────────────────────

REQUIRED_TOOL_COMMANDS = [
    "slug",
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


# ── 7. Constraints ──────────────────────────────────────────────────────

class TestConstraints:
    """Validate constraints cover key rules."""

    def test_every_experiment_has_claim(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "target_claim" in constraints or "关联 claim" in constraints

    def test_success_criterion_quantified(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "量化" in constraints or "数值" in constraints or "quantif" in constraints.lower()

    def test_minimum_seeds(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "3" in constraints and ("seed" in constraints.lower() or "seeds" in constraints.lower())

    def test_no_duplicate_experiments(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "重复" in constraints or "duplicate" in constraints.lower()

    def test_graph_edges_via_tool(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "research_wiki.py" in constraints or "edges.jsonl" in constraints

    def test_slug_uniqueness(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "slug" in constraints.lower() and ("唯一" in constraints or "unique" in constraints.lower())


# ── 8. Error handling ────────────────────────────────────────────────────

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_idea_not_found(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "找不到" in errors or "not found" in errors.lower()

    def test_claim_not_exists(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "claim" in errors.lower() and ("不存在" in errors or "not exist" in errors.lower() or "创建" in errors)

    def test_similar_experiment_exists(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "已有" in errors or "exist" in errors.lower()

    def test_review_llm_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("Review LLM" in errors or "review llm" in errors.lower() or "llm-review" in errors) and ("不可用" in errors or "unavailable" in errors.lower())

    def test_budget_insufficient(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "budget" in errors.lower() or "预算" in errors

    def test_slug_conflict(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "slug" in errors.lower() and ("冲突" in errors or "conflict" in errors.lower())


# ── 9. Review LLM integration ────────────────────────────────────────────────

class TestLLMReviewIntegration:
    """Validate Review LLM MCP server integration for optional review."""

    def test_llm_review_chat_referenced(self, skill_text):
        assert "mcp__llm-review__chat" in skill_text

    def test_review_is_optional(self, skill_text):
        assert "--review" in skill_text

    def test_reviewer_independence_referenced(self, skill_text):
        assert "cross-model-review.md" in skill_text

    def test_reviewer_independence_file_exists(self):
        path = SHARED_REFS / "cross-model-review.md"
        assert path.exists(), f"cross-model-review.md not found at {path}"


# ── 10. CLAUDE.md consistency ────────────────────────────────────────────

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_skill_listed_in_claude_md(self, claude_md_text):
        assert "exp-design" in claude_md_text, \
            "/exp-design must be listed in product CLAUDE.md skills table"

    def test_uses_wikilink_syntax(self, skill_text):
        assert "[[" in skill_text, "Must use wikilink syntax [[slug]]"

    def test_experiment_template_fields(self, skill_text):
        """Experiment pages must include required CLAUDE.md fields."""
        for field in ["status: planned", "target_claim", "hypothesis", "setup", "metrics"]:
            assert field in skill_text, \
                f"Experiment template must include field: {field}"

    def test_edge_type_valid(self, skill_text):
        """tested_by must be a valid edge type per CLAUDE.md."""
        valid_types = {
            "extends", "contradicts", "supports", "inspired_by",
            "tested_by", "invalidates", "supersedes", "addresses_gap", "derived_from",
        }
        graph = _extract_section(skill_text, "Graph edges", level=3)
        found_types = re.findall(r"`(\w+)`", graph)
        for t in found_types:
            if t in valid_types:
                return  # At least one valid edge type found
        assert False, "No valid edge types found in Graph edges section"

    def test_log_format(self, skill_text):
        assert "log wiki/" in skill_text or "log" in skill_text.lower()


# ── 11. Inputs ──────────────────────────────────────────────────────────

class TestInputs:
    """Validate input parameters are documented."""

    def test_idea_slug_input(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "slug" in inputs.lower() or "idea" in inputs.lower()

    def test_review_flag(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "--review" in inputs

    def test_budget_flag(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "--budget" in inputs

    def test_free_text_input(self, skill_text):
        inputs = _extract_section(skill_text, "Inputs", level=2)
        assert "自由文本" in inputs or "free" in inputs.lower() or "假设" in inputs


# ── 12. Output report ──────────────────────────────────────────────────

class TestOutputReport:
    """Validate the experiment plan report format."""

    def test_report_includes_scoped_claims(self, skill_text):
        assert "Scoped Claims" in skill_text or "界定" in skill_text

    def test_report_includes_experiment_blocks(self, skill_text):
        assert "Experiment Blocks" in skill_text or "experiment block" in skill_text.lower()

    def test_report_includes_run_order(self, skill_text):
        assert "Run Order" in skill_text or "run order" in skill_text.lower()

    def test_report_includes_budget(self, skill_text):
        assert "Budget" in skill_text or "budget" in skill_text.lower()

    def test_report_suggests_next_steps(self, skill_text):
        assert "Next Steps" in skill_text or "next step" in skill_text.lower()

    def test_report_suggests_run_experiment(self, skill_text):
        assert "/exp-run" in skill_text


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

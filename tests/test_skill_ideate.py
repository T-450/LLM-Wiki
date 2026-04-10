"""Tests for /ideate SKILL.md structural completeness.

Validates that the ideate skill follows extending.md structure,
implements the 5-phase pipeline, references correct tools/skills/MCP,
and aligns with product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "ideate" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"ideate SKILL.md not found at {SKILL_PATH}"
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
        assert re.search(r"^# /ideate", skill_text, re.MULTILINE)

    def test_has_intro_paragraph(self, skill_text):
        assert re.search(r"^>", skill_text, re.MULTILINE)

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, skill_text, section):
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: ## {section}"


# ── 2. Wiki Interaction ──────────────────────────────────────────────

class TestWikiInteraction:
    """Validate wiki interactions are fully documented."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE)

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE)

    def test_has_graph_edges_subsection(self, skill_text):
        assert re.search(r"^###\s+Graph edges", skill_text, re.MULTILINE)

    @pytest.mark.parametrize("read_target", [
        "context_brief.md", "open_questions.md", "ideas/", "claims/",
        "papers/", "concepts/", "topics/", "experiments/",
    ])
    def test_reads_documented(self, skill_text, read_target):
        reads = _extract_section(skill_text, "Reads", level=3)
        assert read_target in reads, f"Must document reading {read_target}"

    def test_writes_ideas(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "ideas/" in writes

    def test_writes_edges(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "edges.jsonl" in writes

    def test_writes_query_pack(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "context_brief.md" in writes

    def test_writes_gap_map(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "open_questions.md" in writes

    def test_writes_log(self, skill_text):
        writes = _extract_section(skill_text, "Writes", level=3)
        assert "log.md" in writes

    @pytest.mark.parametrize("edge_type", ["addresses_gap", "inspired_by"])
    def test_graph_edge_types(self, skill_text, edge_type):
        graph = _extract_section(skill_text, "Graph edges", level=3)
        assert edge_type in graph, f"Must create {edge_type} edges"


# ── 3. 5-Phase Pipeline ─────────────────────────────────────────────


class TestPipeline:
    """Validate the 5-phase pipeline structure."""

    def test_phase_exists(self, skill_text, ideate_phase_keywords):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        for phase, keyword in ideate_phase_keywords:
            assert phase in workflow, f"Missing {phase} in workflow"
            assert keyword in workflow, f"Phase content must contain '{keyword}'"

    def test_phase_count(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        phases = re.findall(r"Phase \d+", workflow)
        unique_phases = set(phases)
        assert len(unique_phases) >= 5, f"Expected >= 5 phases, found {len(unique_phases)}"


# ── 4. Phase 1: Landscape Scan ──────────────────────────────────────

class TestPhase1LandscapeScan:
    """Validate Phase 1 landscape scan implementation."""

    def test_reads_query_pack(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "context_brief.md" in workflow

    def test_reads_gap_map(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "open_questions.md" in workflow

    def test_loads_banlist(self, skill_text):
        """Must load failed ideas as banlist."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "banlist" in workflow.lower() or "ban" in workflow.lower()

    def test_loads_failed_ideas(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "failed" in workflow.lower() and "failure_reason" in workflow

    def test_websearch(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "WebSearch" in workflow

    def test_semantic_scholar(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "fetch_s2" in workflow or "Semantic Scholar" in workflow

    def test_weak_claims_identified(self, skill_text):
        """Must identify weakly_supported and challenged claims."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "weakly_supported" in workflow or "challenged" in workflow


# ── 5. Phase 2: Dual-Model Brainstorm ───────────────────────────────

class TestPhase2Brainstorm:
    """Validate Phase 2 dual-model brainstorming."""

    def test_claude_generates_ideas(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "Claude" in workflow and ("6-10" in workflow or "6" in workflow)

    def test_review_llm_generates_ideas(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert ("Review LLM" in workflow or "review llm" in workflow.lower()) and ("4-6" in workflow or "4" in workflow)

    def test_llm_review_mcp_reference(self, skill_text):
        assert "mcp__llm-review__chat" in skill_text

    def test_independence_principle(self, skill_text):
        """Review LLM must not see Claude's ideas (cross-model-review.md)."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert ("独立" in workflow or "independence" in workflow.lower() or
                "independent" in workflow.lower())

    def test_merge_and_dedup(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "去重" in workflow or "dedup" in workflow.lower() or "合并" in workflow


# ── 6. Phase 3: Filter ──────────────────────────────────────────────

class TestPhase3Filter:
    """Validate Phase 3 first-pass filter."""

    def test_feasibility_check(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "可行性" in workflow or "feasibility" in workflow.lower()

    def test_quick_novelty_screen(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "novelty" in workflow.lower() or "新颖" in workflow

    def test_banlist_check(self, skill_text):
        """Must filter against banlist."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "banlist" in workflow.lower() or "淘汰" in workflow

    def test_output_survivors(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "4-6" in workflow or "幸存" in workflow or "survivors" in workflow.lower()


# ── 7. Phase 4: Deep Validation ─────────────────────────────────────

class TestPhase4Validation:
    """Validate Phase 4 deep validation with /novelty and /review."""

    def test_calls_novelty_check(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "novelty" in workflow

    def test_calls_review(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "/review" in workflow

    def test_skip_validation_flag(self, skill_text):
        """Must support --skip-validation to bypass Phase 4."""
        assert "skip-validation" in skill_text or "skip_validation" in skill_text

    def test_scoring_formula(self, skill_text):
        """Must have a scoring/ranking system."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "排名" in workflow or "rank" in workflow.lower() or "得分" in workflow


# ── 8. Phase 5: Write to Wiki ───────────────────────────────────────

class TestPhase5WriteToWiki:
    """Validate Phase 5 wiki write operations."""

    def test_creates_idea_pages(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "wiki/ideas/" in workflow

    def test_uses_slug_tool(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "research_wiki.py" in workflow and "slug" in workflow

    def test_adds_graph_edges(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "add-edge" in workflow

    def test_rebuilds_query_pack(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "rebuild-context-brief" in workflow

    def test_rebuilds_gap_map(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "rebuild-open-questions" in workflow

    def test_appends_log(self, skill_text):
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "log" in workflow

    def test_failed_ideas_written(self, skill_text):
        """Filtered-out ideas must be written with status=failed and failure_reason."""
        workflow = _extract_section(skill_text, "Workflow", level=2)
        assert "failed" in workflow.lower() and "failure_reason" in workflow

    def test_idea_report_output(self, skill_text):
        assert "IDEA_REPORT" in skill_text or "Idea Generation Report" in skill_text


# ── 9. Tool and skill references ────────────────────────────────────

class TestToolReferences:
    """Validate tool and skill references and existence."""

    def test_references_research_wiki_slug(self, skill_text):
        assert "research_wiki.py" in skill_text and "slug" in skill_text

    def test_references_research_wiki_add_edge(self, skill_text):
        assert "add-edge" in skill_text

    def test_references_research_wiki_rebuild(self, skill_text):
        assert "rebuild-context-brief" in skill_text
        assert "rebuild-open-questions" in skill_text

    def test_references_fetch_s2(self, skill_text):
        assert "fetch_s2.py" in skill_text

    def test_research_wiki_exists(self):
        assert (TOOLS_DIR / "research_wiki.py").exists()

    def test_fetch_s2_exists(self):
        assert (TOOLS_DIR / "fetch_s2.py").exists()

    def test_references_fetch_deepxiv_search(self, skill_text):
        assert "fetch_deepxiv.py search" in skill_text

    def test_references_fetch_deepxiv_trending(self, skill_text):
        assert "fetch_deepxiv.py trending" in skill_text

    def test_fetch_deepxiv_exists(self):
        assert (TOOLS_DIR / "fetch_deepxiv.py").exists()

    def test_references_novelty_check_skill(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "novelty" in deps

    def test_references_review_skill(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "/review" in deps or "review" in deps

    def test_references_reviewer_independence(self, skill_text):
        assert "cross-model-review.md" in skill_text

    def test_reviewer_independence_exists(self):
        assert (SHARED_REFS / "cross-model-review.md").exists()

    def test_references_websearch(self, skill_text):
        assert "WebSearch" in skill_text

    def test_references_agent_tool(self, skill_text):
        assert "Agent" in skill_text


# ── 10. Constraints ──────────────────────────────────────────────────

class TestConstraints:
    """Validate constraints cover key rules."""

    def test_cold_start_mode(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "cold" in constraints.lower(), \
            "Constraints must describe cold-start mode behavior"

    def test_wiki_evidence_required(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "wiki" in constraints.lower() and (
            "依据" in constraints or "引用" in constraints or
            "grounding" in constraints.lower() or "reference" in constraints.lower()
        )

    def test_banlist_required(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "banlist" in constraints.lower() or "failed" in constraints.lower()

    def test_review_llm_independence(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "独立" in constraints or "independence" in constraints.lower()

    def test_failed_ideas_written(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "failed" in constraints.lower() and ("淘汰" in constraints or "failure_reason" in constraints)

    def test_no_fabrication(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "编造" in constraints or "fabricat" in constraints.lower()

    def test_slug_uniqueness(self, skill_text):
        constraints = _extract_section(skill_text, "Constraints", level=2)
        assert "slug" in constraints.lower()


# ── 11. Error handling ───────────────────────────────────────────────

class TestErrorHandling:
    """Validate error handling covers critical failure modes."""

    def test_empty_wiki(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "wiki" in errors.lower() and ("空" in errors or "empty" in errors.lower())

    def test_websearch_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "WebSearch" in errors

    def test_s2_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "S2" in errors or "Semantic Scholar" in errors

    def test_review_llm_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "Review LLM" in errors or "review llm" in errors.lower() or "llm-review" in errors

    def test_novelty_check_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "novelty" in errors.lower()

    def test_review_failure(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "review" in errors.lower()

    def test_slug_conflict(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "slug" in errors.lower()

    def test_all_ideas_filtered(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert ("淘汰" in errors or "filtered" in errors.lower() or "所有" in errors or
                "eliminated" in errors.lower() or "All ideas" in errors)

    def test_deepxiv_unavailable(self, skill_text):
        errors = _extract_section(skill_text, "Error Handling", level=2)
        assert "deepxiv" in errors.lower() or "DeepXiv" in errors, \
            "Must handle DeepXiv API unavailability with graceful fallback"


# ── 12. CLAUDE.md consistency ────────────────────────────────────────

class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_idea_frontmatter_fields(self, skill_text):
        """Must reference key idea frontmatter fields."""
        for field in ["status", "origin", "origin_gaps", "failure_reason"]:
            assert field in skill_text, f"Must reference idea field '{field}'"

    def test_idea_statuses(self, skill_text):
        """Must use correct idea status values."""
        assert "proposed" in skill_text and "failed" in skill_text

    def test_edge_types_valid(self, skill_text):
        """Edge types used must be from valid set."""
        for edge in ["addresses_gap", "inspired_by"]:
            assert edge in skill_text, f"Must use edge type '{edge}'"

    def test_wikilink_syntax(self, skill_text):
        assert "[[" in skill_text, "Must use wikilink syntax"


# ── 13. Maturity awareness & Growth report ──────────────────────────────

class TestMaturityAwareness:
    """Validate maturity-aware behavior in /ideate."""

    def test_maturity_check_in_prerequisites(self, skill_text):
        assert re.search(r"maturity.*--json", skill_text), \
            "Prerequisites must check wiki maturity via research_wiki.py maturity"

    def test_cold_warm_hot_behaviors(self, skill_text):
        for level in ["cold", "warm", "hot"]:
            assert re.search(rf"\*\*{level}\*\*", skill_text, re.IGNORECASE), \
                f"Must document behavior for maturity level '{level}'"

    def test_maturity_snapshot(self, skill_text):
        assert re.search(r"(maturity_before|Snapshot|snapshot)", skill_text), \
            "Must snapshot maturity at start for Growth Report"

    def test_growth_report_in_output(self, skill_text):
        assert re.search(r"Wiki\s+Growth", skill_text, re.IGNORECASE), \
            "IDEA_REPORT must include Wiki Growth section"

    def test_maturity_tool_in_dependencies(self, skill_text):
        deps = _extract_section(skill_text, "Dependencies", level=2)
        assert "maturity" in deps, \
            "maturity tool must be listed in dependencies"


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

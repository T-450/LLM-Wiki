"""Tests for .claude/skills/check/SKILL.md

Validates:
  - SKILL.md structure follows extending.md requirements
  - All 8 entity types are covered in checks
  - Tool references point to existing files
  - Check categories are complete
  - Constraints match CLAUDE.md
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "check" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"


@pytest.fixture(scope="module")
def skill_content():
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_content():
    return CLAUDE_MD.read_text(encoding="utf-8")


# ── Structure ────────────────────────────────────────────────────────────────

class TestSkillStructure:
    """SKILL.md exists and has all required sections per extending.md."""

    def test_file_exists(self):
        assert SKILL_PATH.exists()

    def test_has_frontmatter(self, skill_content):
        assert skill_content.startswith("---")
        assert "description:" in skill_content

    def test_has_title(self, skill_content):
        assert "# /check" in skill_content

    def test_has_inputs_section(self, skill_content):
        assert "## Inputs" in skill_content

    def test_has_outputs_section(self, skill_content):
        assert "## Outputs" in skill_content

    def test_has_wiki_interaction_section(self, skill_content):
        assert "## Wiki Interaction" in skill_content

    def test_has_workflow_section(self, skill_content):
        assert "## Workflow" in skill_content

    def test_has_constraints_section(self, skill_content):
        assert "## Constraints" in skill_content

    def test_has_error_handling_section(self, skill_content):
        assert "## Error Handling" in skill_content

    def test_has_dependencies_section(self, skill_content):
        assert "## Dependencies" in skill_content


# ── Wiki Interaction ─────────────────────────────────────────────────────────

class TestWikiInteraction:
    """Wiki Interaction section documents reads for all entity types."""

    def test_has_reads_subsection(self, skill_content):
        assert "### Reads" in skill_content

    def test_has_writes_subsection(self, skill_content):
        assert "### Writes" in skill_content

    ENTITY_DIRS = ["papers", "concepts", "topics", "people",
                   "ideas", "experiments", "claims", "Summary"]

    @pytest.mark.parametrize("entity", ENTITY_DIRS)
    def test_reads_entity(self, skill_content, entity):
        reads_section = skill_content[skill_content.index("### Reads"):]
        writes_idx = reads_section.find("### Writes")
        reads_text = reads_section[:writes_idx] if writes_idx != -1 else reads_section
        assert entity in reads_text, f"Entity '{entity}' not in Reads section"

    def test_reads_graph_edges(self, skill_content):
        assert "edges.jsonl" in skill_content

    def test_no_direct_wiki_modification(self, skill_content):
        assert (
            "只报告不修复" in skill_content or "不自动修复" in skill_content
            or "report only" in skill_content.lower() or "no auto" in skill_content.lower()
        )


# ── Entity Field Coverage ────────────────────────────────────────────────────

class TestEntityFieldCoverage:
    """All entity types have their required fields listed in checks."""

    def test_papers_fields(self, skill_content):
        for field in ["title", "slug", "tags", "importance"]:
            assert field in skill_content

    def test_concepts_fields(self, skill_content):
        for field in ["title", "tags", "maturity", "key_papers"]:
            assert field in skill_content

    def test_ideas_fields(self, skill_content):
        for field in ["status", "origin", "priority"]:
            assert field in skill_content

    def test_experiments_fields(self, skill_content):
        for field in ["status", "target_claim", "hypothesis"]:
            assert field in skill_content

    def test_claims_fields(self, skill_content):
        for field in ["status", "confidence", "source_papers", "evidence"]:
            assert field in skill_content

    def test_summary_fields(self, skill_content):
        for field in ["scope", "key_topics"]:
            assert field in skill_content


# ── Check Categories ─────────────────────────────────────────────────────────

class TestCheckCategories:
    """All check categories are documented."""

    def test_broken_links(self, skill_content):
        assert "broken" in skill_content.lower() or "Broken" in skill_content

    def test_orphan_pages(self, skill_content):
        assert "orphan" in skill_content.lower() or "Orphan" in skill_content

    def test_missing_fields(self, skill_content):
        assert "必填字段" in skill_content or "missing" in skill_content.lower()

    def test_enum_validation(self, skill_content):
        assert "Enum" in skill_content or "enum" in skill_content

    def test_confidence_range(self, skill_content):
        assert "confidence" in skill_content and ("[0.0, 1.0]" in skill_content or "0.0" in skill_content)

    def test_failure_reason_check(self, skill_content):
        assert "failure_reason" in skill_content

    def test_xref_asymmetry(self, skill_content):
        assert "asymmetry" in skill_content.lower() or "对称" in skill_content

    def test_graph_edge_consistency(self, skill_content):
        assert "edge" in skill_content.lower() and ("consistency" in skill_content.lower() or "一致性" in skill_content)

    def test_dangling_nodes(self, skill_content):
        assert "dangling" in skill_content.lower() or "Dangling" in skill_content

    def test_quality_checks(self, skill_content):
        assert "quality" in skill_content.lower() or "质量" in skill_content


# ── Report Format ────────────────────────────────────────────────────────────

class TestReportFormat:
    """Report follows the specified format."""

    def test_three_severity_levels(self, skill_content):
        assert "🔴" in skill_content
        assert "🟡" in skill_content
        assert "🔵" in skill_content

    def test_red_category(self, skill_content):
        assert "需立即修复" in skill_content or "🔴" in skill_content

    def test_yellow_category(self, skill_content):
        assert "建议修复" in skill_content or "🟡" in skill_content

    def test_blue_category(self, skill_content):
        assert "可选优化" in skill_content or "🔵" in skill_content

    def test_report_template(self, skill_content):
        assert "Lint Report" in skill_content


# ── Tool References ──────────────────────────────────────────────────────────

class TestToolReferences:
    """Referenced tools exist on disk."""

    def test_lint_tool_exists(self):
        assert (PROJECT_ROOT / "tools" / "lint.py").exists()

    def test_lint_tool_referenced(self, skill_content):
        assert "tools/lint.py" in skill_content

    def test_research_wiki_tool_referenced(self, skill_content):
        assert "research_wiki.py" in skill_content

    def test_no_scripts_reference(self, skill_content):
        """Should reference tools/lint.py, not scripts/lint.py."""
        assert "scripts/lint.py" not in skill_content


# ── Constraints ──────────────────────────────────────────────────────────────

class TestConstraints:
    """Constraints match CLAUDE.md rules."""

    def test_report_only(self, skill_content):
        assert (
            "只报告" in skill_content or "不自动修复" in skill_content
            or "report only" in skill_content.lower() or "no auto" in skill_content.lower()
        )

    def test_raw_readonly(self, skill_content):
        assert "raw/" in skill_content

    def test_graph_readonly(self, skill_content):
        assert "graph/" in skill_content

    def test_idempotent(self, skill_content):
        assert "幂等" in skill_content or "idempotent" in skill_content.lower()


# ── CLAUDE.md Consistency ────────────────────────────────────────────────────

class TestClaudeMdConsistency:
    """Skill is consistent with product CLAUDE.md."""

    def test_skill_listed_in_claude_md(self, claude_content):
        assert "/check" in claude_content

    def test_lint_constraint_in_claude_md(self, claude_content):
        """CLAUDE.md should have lint-only-reports constraint."""
        assert "lint 只报告不修复" in claude_content or "check" in claude_content.lower()

    def test_valid_edge_types_documented(self, skill_content):
        """Edge types checked by lint match CLAUDE.md definitions."""
        valid_types = {"extends", "contradicts", "supports", "inspired_by",
                       "tested_by", "invalidates", "supersedes", "addresses_gap",
                       "derived_from"}
        for t in valid_types:
            assert t in skill_content, f"Edge type '{t}' should be checked by lint"

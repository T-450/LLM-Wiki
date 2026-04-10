"""Tests for /paper-compile SKILL.md structural completeness.

Validates that the paper-compile skill follows extending.md structure,
covers LaTeX compilation + auto-fix + verification + submission checklist,
references correct tools, documents wiki interactions, and aligns with
product CLAUDE.md.
"""

import re
from pathlib import Path

import pytest

# -- Paths -----------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "paper-compile" / "SKILL.md"
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
TOOLS_DIR = PROJECT_ROOT / "tools"
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"


@pytest.fixture(scope="module")
def skill_text():
    assert SKILL_PATH.exists(), f"paper-compile SKILL.md not found at {SKILL_PATH}"
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_md_text():
    assert CLAUDE_MD.exists(), f"Product CLAUDE.md not found at {CLAUDE_MD}"
    return CLAUDE_MD.read_text(encoding="utf-8")


# -- 1. TestSkillStructure ------------------------------------------------

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

    def test_h1_heading(self, skill_text):
        assert re.search(r"^# /paper-compile", skill_text, re.MULTILINE), \
            "Must have '# /paper-compile' heading"

    def test_intro_blockquote(self, skill_text):
        after_h1 = skill_text.split("# /paper-compile", 1)[1]
        lines = after_h1.strip().splitlines()
        found = any(line.strip().startswith(">") for line in lines[:5])
        assert found, "Must have intro blockquote after heading"

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_required_section_present(self, skill_text, section):
        pattern = rf"^##{{1,3}}\s+{re.escape(section)}"
        assert re.search(pattern, skill_text, re.MULTILINE), \
            f"Missing required section: {section}"

    def test_frontmatter_has_argument_hint(self, skill_text):
        fm = skill_text.split("---", 2)[1]
        assert "argument-hint:" in fm, "Frontmatter must include argument-hint"

    def test_argument_hint_mentions_fix(self, skill_text):
        fm = skill_text.split("---", 2)[1]
        assert "--fix" in fm, "argument-hint should mention --fix flag"


# -- 2. TestWikiInteraction ------------------------------------------------


class TestWikiInteraction:
    """Validate Reads/Writes/Graph subsections."""

    def test_has_reads_subsection(self, skill_text):
        assert re.search(r"^###\s+Reads", skill_text, re.MULTILINE)

    def test_has_writes_subsection(self, skill_text):
        assert re.search(r"^###\s+Writes", skill_text, re.MULTILINE)

    def test_has_graph_edges_subsection(self, skill_text):
        assert re.search(r"^###\s+Graph edges", skill_text, re.MULTILINE)

    def test_reads_paper_plan(self, skill_text):
        assert "paper-plan" in skill_text, "Should read paper-plan output for venue info"

    def test_reads_citation_discipline(self, skill_text):
        assert "citation-verification.md" in skill_text, \
            "Should reference citation-verification.md for [UNCONFIRMED] rules"

    def test_writes_main_pdf(self, skill_text):
        assert "main.pdf" in skill_text, "Should produce paper/main.pdf"

    def test_writes_log_md(self, skill_text):
        assert "log.md" in skill_text, "Should append to wiki/log.md"

    def test_graph_edges_none(self, skill_text):
        graph_section = re.split(r"###\s+Graph edges", skill_text, maxsplit=1)
        assert len(graph_section) == 2
        # The graph section should indicate no edges are created
        after = graph_section[1].split("##")[0]  # up to next section
        assert re.search(r"无|none|no\s+edges", after, re.IGNORECASE), \
            "Graph edges should be none"


# -- 3. TestWorkflow -------------------------------------------------------


class TestWorkflow:
    """Validate workflow has 4 steps with correct content."""

    def test_has_step_1_compile(self, skill_text):
        assert re.search(r"Step\s*1.*[Cc]ompil", skill_text), \
            "Step 1 should be compilation"

    def test_has_step_2_auto_fix(self, skill_text):
        assert re.search(r"Step\s*2.*([Aa]uto|[Ff]ix)", skill_text), \
            "Step 2 should be auto-fix"

    def test_has_step_3_verify(self, skill_text):
        assert re.search(r"Step\s*3.*[Vv]erif", skill_text), \
            "Step 3 should be verification"

    def test_has_step_4_report(self, skill_text):
        assert re.search(r"Step\s*4.*([Rr]eport|[Cc]hecklist|清单|报告)", skill_text), \
            "Step 4 should be report/checklist generation"

    def test_step2_missing_package(self, skill_text):
        assert re.search(r"[Mm]issing package", skill_text), \
            "Step 2 should handle missing packages"

    def test_step2_undefined_reference(self, skill_text):
        assert re.search(r"[Uu]ndefined reference", skill_text), \
            "Step 2 should handle undefined references"

    def test_step2_undefined_citation(self, skill_text):
        assert re.search(r"[Uu]ndefined citation", skill_text), \
            "Step 2 should handle undefined citations"

    def test_step2_missing_figure(self, skill_text):
        assert re.search(r"[Mm]issing figure", skill_text), \
            "Step 2 should handle missing figures"

    def test_step2_syntax_error(self, skill_text):
        assert re.search(r"[Ss]yntax error", skill_text), \
            "Step 2 should handle syntax errors"

    def test_mentions_latexmk_command(self, skill_text):
        assert "latexmk" in skill_text, "Should mention latexmk command"

    def test_mentions_pdfinfo(self, skill_text):
        assert "pdfinfo" in skill_text, "Should mention pdfinfo for page count"

    def test_mentions_pdffonts(self, skill_text):
        assert "pdffonts" in skill_text, "Should mention pdffonts for font check"


# -- 4. TestCompileFeatures ------------------------------------------------


class TestCompileFeatures:
    """Validate compile-specific features are documented."""

    def test_latexmk_pdf_flag(self, skill_text):
        assert "latexmk -pdf" in skill_text, "Should use latexmk -pdf"

    def test_nonstopmode(self, skill_text):
        assert "nonstopmode" in skill_text, \
            "Should use -interaction=nonstopmode"

    def test_max_3_fix_compile_rounds(self, skill_text):
        assert re.search(r"3\s*[轮rounds]|3\s*轮|最多\s*3", skill_text), \
            "Should limit to max 3 fix-compile rounds"

    def test_auto_fix_requires_fix_flag(self, skill_text):
        assert "--fix" in skill_text, "Auto-fix should require --fix flag"

    def test_checklist_mode(self, skill_text):
        assert "--checklist" in skill_text, "Should support --checklist mode"

    def test_pdfinfo_for_page_count(self, skill_text):
        assert re.search(r"pdfinfo.*page|page.*pdfinfo", skill_text, re.IGNORECASE | re.DOTALL), \
            "Should use pdfinfo for page count"

    def test_pdffonts_for_font_check(self, skill_text):
        assert re.search(r"pdffonts.*font|font.*pdffonts", skill_text, re.IGNORECASE | re.DOTALL), \
            "Should use pdffonts for font embedding check"

    def test_tlmgr_for_package_install(self, skill_text):
        assert "tlmgr" in skill_text, "Should mention tlmgr for package installation"


# -- 5. TestVerificationChecks ---------------------------------------------


class TestVerificationChecks:
    """Validate all verification checks are documented."""

    def test_page_count_check(self, skill_text):
        assert re.search(r"[Pp]age\s*(count|数)", skill_text), \
            "Should have page count check"

    def test_anonymous_check(self, skill_text):
        assert re.search(r"[Aa]nonymous|匿名", skill_text), \
            "Should have anonymous check"

    def test_anonymous_checks_author(self, skill_text):
        assert re.search(r"\\author|author", skill_text), \
            "Anonymous check should scan for author info"

    def test_anonymous_checks_github_links(self, skill_text):
        assert re.search(r"[Gg]it[Hh]ub", skill_text), \
            "Anonymous check should scan for GitHub links"

    def test_verify_citation_check(self, skill_text):
        assert "[UNCONFIRMED]" in skill_text, "Should check for [UNCONFIRMED] markers"

    def test_unconfirmed_is_hard_blocker(self, skill_text):
        assert re.search(r"\[UNCONFIRMED\].*阻塞|blocker.*\[UNCONFIRMED\]|\[UNCONFIRMED\].*block", skill_text,
                         re.IGNORECASE | re.DOTALL), \
            "[UNCONFIRMED] should be a hard blocker"

    def test_font_embedding_check(self, skill_text):
        assert re.search(r"[Ff]ont.*emb|字体.*嵌入", skill_text), \
            "Should check font embedding"

    def test_todo_fixme_check(self, skill_text):
        assert "TODO" in skill_text and "FIXME" in skill_text, \
            "Should check for TODO/FIXME markers"

    def test_missing_figure_check_in_verify(self, skill_text):
        assert re.search(r"missingfigure|\\missingfigure", skill_text), \
            "Should check for missing figures in verification"

    def test_abstract_presence_check(self, skill_text):
        assert re.search(r"[Aa]bstract", skill_text), \
            "Should check abstract presence"

    def test_check_status_pass_fail(self, skill_text):
        assert "PASS" in skill_text and "FAIL" in skill_text, \
            "Checks should have PASS/FAIL status"

    def test_check_status_warn(self, skill_text):
        assert "WARN" in skill_text, "Some checks should have WARN status"


# -- 6. TestSubmissionChecklist --------------------------------------------


class TestSubmissionChecklist:
    """Validate submission checklist generation."""

    def test_generates_submission_checklist(self, skill_text):
        assert re.search(r"[Ss]ubmission\s+[Cc]hecklist", skill_text), \
            "Should generate submission checklist"

    def test_checklist_pdf_compiles(self, skill_text):
        assert re.search(r"PDF\s+compiles", skill_text), \
            "Checklist should include PDF compilation status"

    def test_checklist_page_count(self, skill_text):
        assert re.search(r"[Pp]age\s+count.*venue|venue.*page", skill_text, re.DOTALL), \
            "Checklist should include page count vs venue limit"

    def test_checklist_unconfirmed_resolved(self, skill_text):
        assert re.search(r"\[UNCONFIRMED\].*resolved|resolved.*\[UNCONFIRMED\]", skill_text,
                         re.IGNORECASE | re.DOTALL), \
            "Checklist should include [UNCONFIRMED] resolution"

    def test_checklist_fonts_embedded(self, skill_text):
        assert re.search(r"[Ff]onts\s+embedded", skill_text), \
            "Checklist should include fonts embedded"

    def test_blocking_issues_section(self, skill_text):
        assert re.search(r"[Bb]locking\s+[Ii]ssues", skill_text), \
            "Should list blocking issues separately"

    def test_warnings_section(self, skill_text):
        assert re.search(r"[Ww]arnings.*non.blocking|non.blocking.*[Ww]arnings", skill_text,
                         re.DOTALL), \
            "Should list warnings separately"


# -- 7. TestConstraints ----------------------------------------------------


class TestConstraints:
    """Validate documented constraints."""

    def test_no_wiki_content_modification(self, skill_text):
        assert re.search(r"不修改\s*wiki|only.*paper/|只操作\s*paper", skill_text,
                         re.IGNORECASE), \
            "Should not modify wiki content (except log.md)"

    def test_auto_fix_requires_flag(self, skill_text):
        constraints = skill_text.split("## Constraints")[1].split("##")[0] if "## Constraints" in skill_text else ""
        assert "--fix" in constraints, "Constraints should state auto-fix requires --fix"

    def test_verify_hard_blocker_in_constraints(self, skill_text):
        constraints = skill_text.split("## Constraints")[1].split("##")[0] if "## Constraints" in skill_text else ""
        assert "[UNCONFIRMED]" in constraints, \
            "Constraints should mention [UNCONFIRMED] as hard blocker"

    def test_max_3_rounds_in_constraints(self, skill_text):
        constraints = skill_text.split("## Constraints")[1].split("##")[0] if "## Constraints" in skill_text else ""
        assert "3" in constraints, "Constraints should mention max 3 fix rounds"

    def test_no_delete_user_content(self, skill_text):
        assert re.search(r"不删除|not\s+delete|不删除用户", skill_text, re.IGNORECASE), \
            "Should not delete user content"

    def test_pdfinfo_pdffonts_optional(self, skill_text):
        assert re.search(r"pdfinfo.*pdffonts.*未安装|tool not available|跳过|optional",
                         skill_text, re.IGNORECASE | re.DOTALL), \
            "pdfinfo/pdffonts should be optional (skip if not installed)"

    def test_anonymous_check_heuristic(self, skill_text):
        assert re.search(r"匿名.*启发|heuristic|WARN.*FAIL|WARN\s+而非\s+FAIL", skill_text,
                         re.IGNORECASE | re.DOTALL), \
            "Anonymous check should be heuristic (WARN not FAIL)"


# -- 8. TestErrorHandling --------------------------------------------------


class TestErrorHandling:
    """Validate error handling scenarios."""

    def test_main_tex_not_found(self, skill_text):
        assert re.search(r"main\.tex.*不存在|main\.tex.*not\s+found", skill_text,
                         re.IGNORECASE), \
            "Should handle main.tex not found"

    def test_latexmk_not_installed(self, skill_text):
        assert re.search(r"latexmk.*未安装|latexmk.*not\s+installed", skill_text,
                         re.IGNORECASE), \
            "Should handle latexmk not installed"

    def test_compile_failure(self, skill_text):
        assert re.search(r"编译失败|compile.*fail|无法.*修复", skill_text,
                         re.IGNORECASE), \
            "Should handle compile failure"

    def test_pdfinfo_pdffonts_not_installed(self, skill_text):
        assert re.search(r"pdfinfo.*pdffonts.*未安装|pdfinfo.*not\s+installed", skill_text,
                         re.IGNORECASE | re.DOTALL), \
            "Should handle pdfinfo/pdffonts not installed"

    def test_paper_plan_not_found(self, skill_text):
        assert re.search(r"PAPER_PLAN.*找不到|paper.plan.*not\s+found", skill_text,
                         re.IGNORECASE), \
            "Should handle PAPER_PLAN not found"


# -- 9. TestToolReferences -------------------------------------------------


class TestToolReferences:
    """Validate references to external tools and native capabilities."""

    def test_references_latexmk(self, skill_text):
        assert "latexmk" in skill_text, "Should reference latexmk"

    def test_references_pdfinfo(self, skill_text):
        assert "pdfinfo" in skill_text, "Should reference pdfinfo"

    def test_references_pdffonts(self, skill_text):
        assert "pdffonts" in skill_text, "Should reference pdffonts"

    def test_references_research_wiki_log(self, skill_text):
        assert re.search(r"research_wiki\.py\s+log", skill_text), \
            "Should use research_wiki.py log for logging"

    def test_uses_native_read(self, skill_text):
        assert re.search(r"`Read`|Read\b.*read", skill_text), \
            "Should use Claude Code native Read"

    def test_uses_native_bash(self, skill_text):
        assert re.search(r"`Bash`|Bash\b.*execute|Bash\b.*command", skill_text), \
            "Should use Claude Code native Bash"

    def test_uses_native_edit(self, skill_text):
        assert re.search(r"`Edit`", skill_text), \
            "Should use Claude Code native Edit for auto-fix"

    def test_uses_native_grep(self, skill_text):
        assert re.search(r"`Grep`", skill_text), \
            "Should use Claude Code native Grep"


# -- 10. TestSharedReferences ----------------------------------------------


class TestSharedReferences:
    """Validate shared reference files are referenced and exist."""

    def test_citation_discipline_referenced(self, skill_text):
        assert "citation-verification.md" in skill_text, \
            "Should reference citation-verification.md"

    def test_citation_discipline_exists(self):
        path = SHARED_REFS / "citation-verification.md"
        assert path.exists(), f"citation-verification.md must exist at {path}"

    def test_writing_principles_referenced(self, skill_text):
        assert "academic-writing.md" in skill_text, \
            "Should reference academic-writing.md"

    def test_writing_principles_exists(self):
        path = SHARED_REFS / "academic-writing.md"
        assert path.exists(), f"academic-writing.md must exist at {path}"

    def test_no_mcp_servers_needed(self, skill_text):
        deps = skill_text.split("## Dependencies")[1] if "## Dependencies" in skill_text else ""
        mcp_section = ""
        if "MCP" in deps:
            mcp_start = deps.index("MCP")
            mcp_section = deps[mcp_start:mcp_start + 200]
        assert re.search(r"无|[Nn]one|no\s+MCP", mcp_section) or "MCP" not in deps, \
            "Should not require MCP servers"


# -- 11. TestClaudeMdConsistency -------------------------------------------


class TestClaudeMdConsistency:
    """Validate alignment with product CLAUDE.md."""

    def test_paper_compile_in_claude_md(self, claude_md_text):
        assert re.search(r"paper.compile", claude_md_text), \
            "/paper-compile should be referenced in product CLAUDE.md"

    def test_log_format_matches(self, skill_text):
        # The skill should use the standard log format via tools/research_wiki.py
        assert re.search(r"research_wiki\.py\s+log\s+wiki/", skill_text), \
            "Log call should match standard format: research_wiki.py log wiki/ ..."

    def test_no_review_llm_dependency(self, skill_text):
        deps = skill_text.split("## Dependencies")[1].split("##")[0] if "## Dependencies" in skill_text else ""
        mcp_match = re.search(r"###\s*MCP", deps)
        if mcp_match:
            mcp_section = deps[mcp_match.start():mcp_match.start() + 200]
            assert re.search(r"无|[Nn]one", mcp_section), \
                "paper-compile should not depend on Review LLM"
        # If no MCP section header found, that's also fine

    def test_outputs_directory_mentioned(self, skill_text):
        assert re.search(r"paper/", skill_text), \
            "Should operate on paper/ directory"

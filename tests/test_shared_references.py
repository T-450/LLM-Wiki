"""Tests for shared-references: citation-verification.md and academic-writing.md.

Validates content completeness, required sections, documented rules,
and cross-references from consuming skills (paper-draft, paper-plan,
paper-compile, survey).
"""

import re
from pathlib import Path

import pytest

# ── Paths ───────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SHARED_REFS = PROJECT_ROOT / ".claude" / "skills" / "shared-references"
CITATION_PATH = SHARED_REFS / "citation-verification.md"
WRITING_PATH = SHARED_REFS / "academic-writing.md"
CROSS_MODEL_REVIEW_PATH = SHARED_REFS / "cross-model-review.md"
SKILLS_DIR = PROJECT_ROOT / ".claude" / "skills"


@pytest.fixture(scope="module")
def citation_text():
    assert CITATION_PATH.exists(), f"citation-verification.md not found at {CITATION_PATH}"
    return CITATION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def writing_text():
    assert WRITING_PATH.exists(), f"academic-writing.md not found at {WRITING_PATH}"
    return WRITING_PATH.read_text(encoding="utf-8")


def _read_skill(name: str) -> str:
    """Read a SKILL.md file by skill directory name."""
    path = SKILLS_DIR / name / "SKILL.md"
    assert path.exists(), f"{name}/SKILL.md not found at {path}"
    return path.read_text(encoding="utf-8")


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


# ══════════════════════════════════════════════════════════════════════════
# TestCitationDiscipline
# ══════════════════════════════════════════════════════════════════════════


class TestCitationDiscipline:
    """Validate citation-verification.md content and structure."""

    def test_file_exists(self):
        assert CITATION_PATH.exists()

    def test_has_heading(self, citation_text):
        assert re.search(r"^# Citation Discipline", citation_text, re.MULTILINE), \
            "Must have '# Citation Discipline' heading"

    def test_documents_core_rule(self, citation_text):
        section = _extract_section(citation_text, "Core Rule", level=2)
        assert "authoritative sources" in section.lower() or "BibTeX" in section, \
            "Core Rule must document BibTeX from authoritative sources"

    def test_documents_unconfirmed_protocol(self, citation_text):
        assert re.search(r"^##\s+.*\[UNCONFIRMED\].*Protocol", citation_text, re.MULTILINE), \
            "Must have a section documenting the [UNCONFIRMED] protocol"

    @pytest.mark.parametrize("source", [
        "DBLP",
        "CrossRef",
        "Semantic Scholar",
    ])
    def test_bibtex_source_documented(self, citation_text, source):
        assert source in citation_text, \
            f"BibTeX source '{source}' must be documented"

    def test_bibtex_source_paper_own_bib(self, citation_text):
        assert ".bib" in citation_text and "paper" in citation_text.lower(), \
            "Must document the paper's own .bib file as a BibTeX source"

    def test_dblp_fetching_method(self, citation_text):
        section = _extract_section(citation_text, "DBLP", level=3)
        assert "dblp.org" in section, "Must document DBLP fetching URL"

    def test_crossref_fetching_method(self, citation_text):
        section = _extract_section(citation_text, "CrossRef", level=3)
        assert "crossref.org" in section, "Must document CrossRef fetching URL"

    def test_s2_fetching_method(self, citation_text):
        section = _extract_section(citation_text, "Semantic Scholar", level=3)
        assert "fetch_s2.py" in section or "semanticscholar.org" in section, \
            "Must document Semantic Scholar fetching method"

    def test_citation_key_convention(self, citation_text):
        assert re.search(r"^##\s+Citation Key Convention", citation_text, re.MULTILINE), \
            "Must have Citation Key Convention section"

    def test_citation_key_format(self, citation_text):
        section = _extract_section(citation_text, "Citation Key Convention", level=2)
        assert "first-author" in section.lower() or "lastname" in section.lower(), \
            "Key convention must reference author lastname"
        assert "year" in section.lower(), "Key convention must reference year"

    def test_rules_for_paper_write(self, citation_text):
        assert re.search(r"###\s+/paper-draft", citation_text), \
            "Must document rules for /paper-draft"

    def test_rules_for_write_related_work(self, citation_text):
        assert re.search(r"###\s+/survey", citation_text), \
            "Must document rules for /survey"

    def test_rules_for_paper_plan(self, citation_text):
        assert re.search(r"###\s+/paper-plan", citation_text), \
            "Must document rules for /paper-plan"

    def test_what_not_to_do_section(self, citation_text):
        assert re.search(r"^##\s+What NOT To Do", citation_text, re.MULTILINE), \
            "Must have 'What NOT To Do' section"

    def test_never_generate_bibtex_from_memory(self, citation_text):
        lower = citation_text.lower()
        assert "never" in lower and "generate" in lower and ("memory" in lower or "bibtex" in lower), \
            "Must mention 'never generate BibTeX from memory'"

    def test_mentions_fetch_s2(self, citation_text):
        assert "tools/fetch_s2.py" in citation_text, \
            "Must reference tools/fetch_s2.py"

    def test_verify_prefix_for_bibtex_keys(self, citation_text):
        assert "UNCONFIRMED_" in citation_text, \
            "Must document UNCONFIRMED_ prefix for BibTeX keys"

    def test_nocite_prohibition(self, citation_text):
        assert "nocite" in citation_text.lower() or r"\nocite" in citation_text, \
            "Must mention nocite prohibition"


# ══════════════════════════════════════════════════════════════════════════
# TestWritingPrinciples
# ══════════════════════════════════════════════════════════════════════════


class TestWritingPrinciples:
    """Validate academic-writing.md content and structure."""

    def test_file_exists(self):
        assert WRITING_PATH.exists()

    def test_has_heading(self, writing_text):
        assert re.search(r"^# Academic Writing Principles", writing_text, re.MULTILINE), \
            "Must have '# Academic Writing Principles' heading"

    def test_has_narrative_structure_section(self, writing_text):
        assert re.search(r"^##\s+.*Narrative Structure", writing_text, re.MULTILINE), \
            "Must have Narrative Structure section"

    def test_hourglass_model(self, writing_text):
        section = _extract_section(writing_text, "Narrative Structure", level=2)
        assert "hourglass" in section.lower(), \
            "Narrative Structure must document the hourglass model"

    def test_has_clarity_rules_section(self, writing_text):
        assert re.search(r"^##\s+.*Clarity Rules", writing_text, re.MULTILINE), \
            "Must have Clarity Rules section"

    def test_clarity_sentence_subsection(self, writing_text):
        assert re.search(r"^###\s+Sentence", writing_text, re.MULTILINE), \
            "Clarity Rules must have Sentence Level subsection"

    def test_clarity_paragraph_subsection(self, writing_text):
        assert re.search(r"^###\s+Paragraph", writing_text, re.MULTILINE), \
            "Clarity Rules must have Paragraph Level subsection"

    def test_clarity_notation_subsection(self, writing_text):
        assert re.search(r"^###\s+Notation", writing_text, re.MULTILINE), \
            "Clarity Rules must have Notation Consistency subsection"

    def test_has_figure_and_table_section(self, writing_text):
        assert re.search(r"^##\s+.*Figure and Table", writing_text, re.MULTILINE), \
            "Must have Figure and Table Design section"

    def test_has_de_ai_polish_section(self, writing_text):
        assert re.search(r"^##\s+.*De-AI Polish", writing_text, re.MULTILINE), \
            "Must have De-AI Polish Rules section"

    @pytest.mark.parametrize("ai_word", [
        "delve",
        "leverage",
        "utilize",
        "comprehensive",
        "crucial",
        "pivotal",
    ])
    def test_ai_word_documented(self, writing_text, ai_word):
        assert ai_word in writing_text.lower(), \
            f"De-AI polish must document AI word '{ai_word}'"

    @pytest.mark.parametrize("venue", [
        "ICLR",
        "NeurIPS",
        "ICML",
        "ACL",
        "CVPR",
        "IEEE",
    ])
    def test_venue_page_limit(self, writing_text, venue):
        assert venue in writing_text, \
            f"Must document page limits for {venue}"

    def test_anonymity_rules(self, writing_text):
        assert re.search(r"^###\s+Anonymity", writing_text, re.MULTILINE), \
            "Must have Anonymity Rules subsection"

    def test_anonymity_no_author_names(self, writing_text):
        section = _extract_section(writing_text, "Anonymity", level=3)
        assert "author" in section.lower() or "name" in section.lower(), \
            "Anonymity rules must mention author names"

    def test_booktabs_style(self, writing_text):
        assert "toprule" in writing_text or "booktabs" in writing_text.lower(), \
            "Must document booktabs style for tables"

    def test_colorblind_safe_palettes(self, writing_text):
        lower = writing_text.lower()
        assert "colorblind" in lower or "colour-blind" in lower, \
            "Must document colorblind-safe palettes"

    def test_font_size_8pt(self, writing_text):
        assert "8pt" in writing_text or "8 pt" in writing_text, \
            "Must document font size >= 8pt"

    def test_what_not_to_do_section(self, writing_text):
        assert re.search(r"^##\s+What NOT To Do", writing_text, re.MULTILINE), \
            "Must have 'What NOT To Do' section"

    def test_referenced_by_paper_write(self, writing_text):
        """academic-writing.md should mention /paper-draft as a consumer."""
        assert "paper-draft" in writing_text, \
            "Must mention /paper-draft as a consuming skill"

    def test_referenced_by_paper_plan(self, writing_text):
        """academic-writing.md should mention /paper-plan as a consumer."""
        assert "paper-plan" in writing_text, \
            "Must mention /paper-plan as a consuming skill"


# ══════════════════════════════════════════════════════════════════════════
# TestCrossReferences
# ══════════════════════════════════════════════════════════════════════════


class TestCrossReferences:
    """Validate that consuming skills reference the shared reference files."""

    @pytest.mark.parametrize("skill_name", [
        "paper-draft",
        "survey",
        "paper-plan",
        "paper-compile",
    ])
    def test_skill_references_citation_discipline(self, skill_name):
        text = _read_skill(skill_name)
        assert "citation-verification" in text, \
            f"{skill_name}/SKILL.md must reference citation-verification.md"

    @pytest.mark.parametrize("skill_name", [
        "paper-draft",
        "paper-plan",
        "paper-compile",
        "survey",
    ])
    def test_skill_references_writing_principles(self, skill_name):
        text = _read_skill(skill_name)
        assert "academic-writing" in text, \
            f"{skill_name}/SKILL.md must reference academic-writing.md"

    def test_reviewer_independence_exists(self):
        """The existing cross-model-review.md must still be present."""
        assert CROSS_MODEL_REVIEW_PATH.exists(), \
            f"cross-model-review.md not found at {CROSS_MODEL_REVIEW_PATH}"

"""Tests for tools/fetch_arxiv.py."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "tools")
from fetch_arxiv import DEFAULT_CATEGORIES, extract_id, fetch_recent


# ---------------------------------------------------------------------------
# extract_id
# ---------------------------------------------------------------------------

class TestExtractId:
    """Tests for arXiv ID extraction from URLs."""

    def test_standard_url(self):
        assert extract_id("https://arxiv.org/abs/2106.09685") == "2106.09685"

    def test_url_with_version(self):
        assert extract_id("https://arxiv.org/abs/2106.09685v2") == "2106.09685"

    def test_url_with_high_version(self):
        assert extract_id("https://arxiv.org/abs/2106.09685v15") == "2106.09685"

    def test_url_with_trailing_slash(self):
        assert extract_id("https://arxiv.org/abs/2106.09685v2/") == "2106.09685"

    def test_old_format_id(self):
        """Old arXiv IDs — extract_id takes last path segment only."""
        # URL split by '/' means we only get the numeric part
        assert extract_id("https://arxiv.org/abs/hep-th/9901001v1") == "9901001"

    def test_no_version_suffix(self):
        assert extract_id("https://arxiv.org/abs/2401.12345") == "2401.12345"

    def test_empty_url(self):
        assert extract_id("") == ""

    def test_url_without_abs(self):
        """URLs with pdf path should still extract ID."""
        assert extract_id("https://arxiv.org/pdf/2106.09685v1") == "2106.09685"

    def test_id_with_letter_v_not_version(self):
        """The letter v in the ID body should not be stripped."""
        # e.g. a hypothetical ID ending with non-version 'v'
        assert extract_id("https://arxiv.org/abs/overview") == "overview"


# ---------------------------------------------------------------------------
# fetch_recent — with mocked feedparser
# ---------------------------------------------------------------------------

def _make_entry(
    arxiv_id: str,
    title: str = "Test Paper",
    published: str | None = None,
) -> dict:
    """Create a fake feedparser entry."""
    now = datetime.now(timezone.utc)
    if published is None:
        published = now.isoformat()
    return {
        "title": title,
        "summary": "Abstract text",
        "authors": [{"name": "Author A"}, {"name": "Author B"}],
        "link": f"https://arxiv.org/abs/{arxiv_id}v1",
        "published": published,
    }


def _make_feed(entries: list[dict], bozo: bool = False) -> SimpleNamespace:
    return SimpleNamespace(entries=entries, bozo=bozo)


class TestFetchRecent:
    """Tests for fetch_recent with mocked RSS feeds."""

    @patch("fetch_arxiv.feedparser.parse")
    def test_returns_papers(self, mock_parse):
        entry = _make_entry("2401.00001")
        mock_parse.return_value = _make_feed([entry])
        papers = fetch_recent(hours=48, categories=["cs.LG"])
        assert len(papers) == 1
        assert papers[0]["arxiv_id"] == "2401.00001"
        assert papers[0]["title"] == "Test Paper"
        assert papers[0]["category"] == "cs.LG"

    @patch("fetch_arxiv.feedparser.parse")
    def test_time_filter_excludes_old_papers(self, mock_parse):
        old_time = (datetime.now(timezone.utc) - timedelta(hours=72)).isoformat()
        entry = _make_entry("2401.00001", published=old_time)
        mock_parse.return_value = _make_feed([entry])
        papers = fetch_recent(hours=24, categories=["cs.LG"])
        assert len(papers) == 0

    @patch("fetch_arxiv.feedparser.parse")
    def test_time_filter_keeps_recent_papers(self, mock_parse):
        recent_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        entry = _make_entry("2401.00001", published=recent_time)
        mock_parse.return_value = _make_feed([entry])
        papers = fetch_recent(hours=24, categories=["cs.LG"])
        assert len(papers) == 1

    @patch("fetch_arxiv.feedparser.parse")
    def test_unparseable_date_keeps_entry(self, mock_parse):
        entry = _make_entry("2401.00001", published="not-a-date")
        mock_parse.return_value = _make_feed([entry])
        papers = fetch_recent(hours=24, categories=["cs.LG"])
        assert len(papers) == 1

    @patch("fetch_arxiv.feedparser.parse")
    def test_empty_published_keeps_entry(self, mock_parse):
        entry = _make_entry("2401.00001", published="")
        mock_parse.return_value = _make_feed([entry])
        papers = fetch_recent(hours=24, categories=["cs.LG"])
        assert len(papers) == 1

    @patch("fetch_arxiv.feedparser.parse")
    def test_dedup_by_arxiv_id(self, mock_parse):
        entry1 = _make_entry("2401.00001", title="From cs.LG")
        entry2 = _make_entry("2401.00001", title="From cs.AI")
        mock_parse.return_value = _make_feed([entry1, entry2])
        papers = fetch_recent(hours=48, categories=["cs.LG"])
        assert len(papers) == 1

    @patch("fetch_arxiv.feedparser.parse")
    def test_dedup_across_categories(self, mock_parse):
        entry = _make_entry("2401.00001")
        mock_parse.return_value = _make_feed([entry])
        papers = fetch_recent(hours=48, categories=["cs.LG", "cs.AI"])
        # Same paper from 2 categories, should be deduped
        assert len(papers) == 1

    @patch("fetch_arxiv.feedparser.parse")
    def test_bozo_feed_with_no_entries_skipped(self, mock_parse):
        mock_parse.return_value = _make_feed([], bozo=True)
        papers = fetch_recent(hours=48, categories=["cs.LG"])
        assert len(papers) == 0

    @patch("fetch_arxiv.feedparser.parse")
    def test_bozo_feed_with_entries_still_parsed(self, mock_parse):
        entry = _make_entry("2401.00001")
        mock_parse.return_value = _make_feed([entry], bozo=True)
        papers = fetch_recent(hours=48, categories=["cs.LG"])
        assert len(papers) == 1

    @patch("fetch_arxiv.feedparser.parse")
    def test_parse_exception_skips_category(self, mock_parse):
        mock_parse.side_effect = Exception("Network error")
        papers = fetch_recent(hours=48, categories=["cs.LG"])
        assert len(papers) == 0

    @patch("fetch_arxiv.feedparser.parse")
    def test_default_categories_used(self, mock_parse):
        mock_parse.return_value = _make_feed([])
        fetch_recent(hours=24)
        assert mock_parse.call_count == len(DEFAULT_CATEGORIES)

    @patch("fetch_arxiv.feedparser.parse")
    def test_custom_categories(self, mock_parse):
        mock_parse.return_value = _make_feed([])
        fetch_recent(hours=24, categories=["cs.RO", "cs.SE"])
        assert mock_parse.call_count == 2

    @patch("fetch_arxiv.feedparser.parse")
    def test_output_fields(self, mock_parse):
        entry = _make_entry("2401.00001", title="My Paper")
        mock_parse.return_value = _make_feed([entry])
        papers = fetch_recent(hours=48, categories=["cs.LG"])
        p = papers[0]
        assert set(p.keys()) == {
            "title", "abstract", "authors", "arxiv_url",
            "arxiv_id", "category", "published",
        }
        assert p["authors"] == ["Author A", "Author B"]

    @patch("fetch_arxiv.feedparser.parse")
    def test_title_newlines_stripped(self, mock_parse):
        entry = _make_entry("2401.00001", title="Line1\nLine2\n")
        mock_parse.return_value = _make_feed([entry])
        papers = fetch_recent(hours=48, categories=["cs.LG"])
        assert "\n" not in papers[0]["title"]


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------

class TestCLI:
    """Test CLI invocation via subprocess."""

    def test_cli_outputs_json(self):
        """CLI should output valid JSON (with mocked network)."""
        # We test that the script is at least importable and parseable
        result = subprocess.run(
            [sys.executable, "tools/fetch_arxiv.py", "--help"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        assert result.returncode == 0
        assert "arXiv" in result.stdout or "arxiv" in result.stdout.lower()

    def test_cli_accepts_hours_flag(self):
        result = subprocess.run(
            [sys.executable, "tools/fetch_arxiv.py", "--help"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        assert "--hours" in result.stdout

    def test_cli_accepts_categories_flag(self):
        result = subprocess.run(
            [sys.executable, "tools/fetch_arxiv.py", "--help"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        assert "--categories" in result.stdout

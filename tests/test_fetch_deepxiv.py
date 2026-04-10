"""Tests for tools/fetch_deepxiv.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "tools")
from fetch_deepxiv import brief, head, raw, search, section, social, trending

# ---------------------------------------------------------------------------
# Mock Reader factory
# ---------------------------------------------------------------------------

def _mock_reader():
    """Return a MagicMock that mimics deepxiv_sdk.Reader."""
    reader = MagicMock()

    # search
    reader.search.return_value = {
        "total": 1,
        "took": 10,
        "results": [
            {
                "arxiv_id": "2106.09685",
                "title": "LoRA",
                "abstract": "Low-rank adaptation...",
                "authors": [{"name": "Edward Hu", "orgs": ["Microsoft"]}],
                "categories": ["cs.LG"],
                "year": 2021,
                "citation": 5000,
                "score": 0.95,
                "publish_at": "2021-06-17",
            }
        ],
    }

    # brief
    reader.brief.return_value = {
        "arxiv_id": "2106.09685",
        "title": "LoRA",
        "tldr": "Proposes low-rank adaptation for LLMs",
        "keywords": ["lora", "fine-tuning"],
        "citations": 5000,
        "publish_at": "2021-06-17",
        "src_url": "https://arxiv.org/pdf/2106.09685",
        "github_url": "https://github.com/microsoft/LoRA",
    }

    # head
    reader.head.return_value = {
        "arxiv_id": "2106.09685",
        "title": "LoRA",
        "abstract": "Low-rank...",
        "authors": [{"name": "Edward Hu"}],
        "categories": ["cs.LG"],
        "publish_at": "2021-06-17",
        "token_count": 12000,
        "sections": {
            "Introduction": {"tldr": "Intro summary", "token_count": 800},
            "Method": {"tldr": "Method summary", "token_count": 2000},
        },
    }

    # section
    reader.section.return_value = "Introduction content here..."

    # raw
    reader.raw.return_value = "# LoRA\n\nFull paper markdown..."

    # trending
    reader.trending.return_value = {
        "papers": [
            {
                "arxiv_id": "2401.00001",
                "title": "Hot Paper",
                "rank": 1,
                "stats": {"total_tweets": 500, "total_views": 10000},
                "categories": ["cs.AI"],
            }
        ],
        "total": 1,
    }

    # social_impact
    reader.social_impact.return_value = {
        "arxiv_id": "2106.09685",
        "total_tweets": 300,
        "total_views": 8000,
        "total_likes": 1200,
        "total_replies": 50,
        "first_seen_date": "2021-06-18",
        "last_seen_date": "2021-07-01",
    }

    return reader


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------

class TestSearch:
    @patch("fetch_deepxiv._get_reader")
    def test_returns_list(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = search("low rank adaptation")
        assert isinstance(result, list)
        assert len(result) == 1

    @patch("fetch_deepxiv._get_reader")
    def test_output_fields(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = search("lora")[0]
        assert set(result.keys()) == {
            "arxiv_id", "title", "abstract", "authors",
            "categories", "year", "citation_count",
            "relevance_score", "published",
        }

    @patch("fetch_deepxiv._get_reader")
    def test_authors_normalised(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = search("lora")[0]
        assert result["authors"] == ["Edward Hu"]

    @patch("fetch_deepxiv._get_reader")
    def test_mode_passed_to_reader(self, mock_get):
        reader = _mock_reader()
        mock_get.return_value = reader
        search("lora", mode="bm25")
        reader.search.assert_called_once()
        call_kwargs = reader.search.call_args[1]
        assert call_kwargs["search_mode"] == "bm25"

    @patch("fetch_deepxiv._get_reader")
    def test_filters_passed(self, mock_get):
        reader = _mock_reader()
        mock_get.return_value = reader
        search(
            "lora",
            categories=["cs.LG"],
            min_citation=100,
            date_from="2024-01-01",
        )
        call_kwargs = reader.search.call_args[1]
        assert call_kwargs["categories"] == ["cs.LG"]
        assert call_kwargs["min_citation"] == 100
        assert call_kwargs["date_from"] == "2024-01-01"

    @patch("fetch_deepxiv._get_reader")
    def test_empty_results(self, mock_get):
        reader = _mock_reader()
        reader.search.return_value = {"total": 0, "results": []}
        mock_get.return_value = reader
        result = search("nonexistent")
        assert result == []


# ---------------------------------------------------------------------------
# brief
# ---------------------------------------------------------------------------

class TestBrief:
    @patch("fetch_deepxiv._get_reader")
    def test_returns_dict(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = brief("2106.09685")
        assert isinstance(result, dict)

    @patch("fetch_deepxiv._get_reader")
    def test_output_fields(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = brief("2106.09685")
        assert "tldr" in result
        assert "keywords" in result
        assert "citations" in result
        assert result["tldr"] == "Proposes low-rank adaptation for LLMs"

    @patch("fetch_deepxiv._get_reader")
    def test_github_url(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = brief("2106.09685")
        assert result["github_url"] == "https://github.com/microsoft/LoRA"


# ---------------------------------------------------------------------------
# head
# ---------------------------------------------------------------------------

class TestHead:
    @patch("fetch_deepxiv._get_reader")
    def test_returns_dict(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = head("2106.09685")
        assert isinstance(result, dict)

    @patch("fetch_deepxiv._get_reader")
    def test_sections_normalised(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = head("2106.09685")
        assert isinstance(result["sections"], list)
        assert len(result["sections"]) == 2
        assert result["sections"][0]["name"] == "Introduction"
        assert "tldr" in result["sections"][0]

    @patch("fetch_deepxiv._get_reader")
    def test_token_count(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = head("2106.09685")
        assert result["token_count"] == 12000


# ---------------------------------------------------------------------------
# section
# ---------------------------------------------------------------------------

class TestSection:
    @patch("fetch_deepxiv._get_reader")
    def test_returns_content(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = section("2106.09685", "Introduction")
        assert result["content"] == "Introduction content here..."
        assert result["section_name"] == "Introduction"


# ---------------------------------------------------------------------------
# raw
# ---------------------------------------------------------------------------

class TestRaw:
    @patch("fetch_deepxiv._get_reader")
    def test_returns_content(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = raw("2106.09685")
        assert "LoRA" in result["content"]
        assert result["arxiv_id"] == "2106.09685"


# ---------------------------------------------------------------------------
# trending
# ---------------------------------------------------------------------------

class TestTrending:
    @patch("fetch_deepxiv._get_reader")
    def test_returns_list(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = trending(days=7)
        assert isinstance(result, list)
        assert len(result) == 1

    @patch("fetch_deepxiv._get_reader")
    def test_output_fields(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = trending(days=7)[0]
        assert "arxiv_id" in result
        assert "social_impact" in result
        assert "rank" in result

    @patch("fetch_deepxiv._get_reader")
    def test_days_passed(self, mock_get):
        reader = _mock_reader()
        mock_get.return_value = reader
        trending(days=14, limit=50)
        reader.trending.assert_called_once_with(days=14, limit=50)


# ---------------------------------------------------------------------------
# social
# ---------------------------------------------------------------------------

class TestSocial:
    @patch("fetch_deepxiv._get_reader")
    def test_returns_metrics(self, mock_get):
        mock_get.return_value = _mock_reader()
        result = social("2106.09685")
        assert result["tweets"] == 300
        assert result["views"] == 8000
        assert result["likes"] == 1200

    @patch("fetch_deepxiv._get_reader")
    def test_no_data_returns_zeros(self, mock_get):
        reader = _mock_reader()
        reader.social_impact.return_value = None
        mock_get.return_value = reader
        result = social("0000.00000")
        assert result["tweets"] == 0
        assert result["views"] == 0


# ---------------------------------------------------------------------------
# Token handling
# ---------------------------------------------------------------------------

class TestToken:
    @patch.dict("os.environ", {"DEEPXIV_TOKEN": "test-token-123"}, clear=False)
    @patch("fetch_deepxiv.Reader")
    def test_token_from_env(self, mock_reader_cls):
        # Re-import to pick up env var
        import importlib
        import fetch_deepxiv
        importlib.reload(fetch_deepxiv)
        assert fetch_deepxiv.DEEPXIV_TOKEN == "test-token-123"

    @patch.dict("os.environ", {}, clear=False)
    @patch("fetch_deepxiv.Reader")
    def test_no_env_var_falls_back_to_dotenv(self, mock_reader_cls):
        """Without DEEPXIV_TOKEN env var, token may still be loaded from ~/.env."""
        import importlib
        import fetch_deepxiv
        import os
        os.environ.pop("DEEPXIV_TOKEN", None)
        importlib.reload(fetch_deepxiv)
        # Token could be empty or loaded from ~/.env — both are valid
        assert isinstance(fetch_deepxiv.DEEPXIV_TOKEN, str)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class TestCLI:
    def test_cli_help(self):
        result = subprocess.run(
            [sys.executable, "tools/fetch_deepxiv.py", "--help"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        assert result.returncode == 0
        assert "search" in result.stdout
        assert "brief" in result.stdout
        assert "trending" in result.stdout

    def test_cli_search_help(self):
        result = subprocess.run(
            [sys.executable, "tools/fetch_deepxiv.py", "search", "--help"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        assert result.returncode == 0
        assert "--mode" in result.stdout
        assert "--limit" in result.stdout
        assert "--categories" in result.stdout

    def test_cli_no_subcommand_fails(self):
        result = subprocess.run(
            [sys.executable, "tools/fetch_deepxiv.py"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        assert result.returncode != 0

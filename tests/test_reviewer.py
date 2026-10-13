import pytest
from backend.reviewer import CodeReviewer


@pytest.fixture
def reviewer():
    return CodeReviewer()


def test_detect_language_python(reviewer):
    assert reviewer._detect_language("script.py") == "python"


def test_detect_language_js(reviewer):
    assert reviewer._detect_language("app.js") == "javascript"


def test_detect_language_unknown(reviewer):
    assert reviewer._detect_language("README") == "python"


def test_format_comment_contains_score(reviewer):
    review = {
        "quality_score": 8,
        "summary": "Nice work",
        "severity": "low",
        "bugs": [],
        "suggestions": ["Add docstring"],
        "security_issues": [],
    }
    comment = reviewer.format_comment(review)
    assert "8/10" in comment
    assert "Nice work" in comment
    assert "Add docstring" in comment


def test_format_comment_high_green(reviewer):
    review = {
        "quality_score": 9,
        "summary": "Great",
        "severity": "low",
        "bugs": [],
        "suggestions": [],
        "security_issues": [],
    }
    assert "🟢" in reviewer.format_comment(review)


def test_format_comment_low_red(reviewer):
    review = {
        "quality_score": 2,
        "summary": "Poor",
        "severity": "critical",
        "bugs": ["null pointer"],
        "suggestions": [],
        "security_issues": [],
    }
    assert "🔴" in reviewer.format_comment(review)

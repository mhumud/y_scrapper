"""Module with tests for the scraper module."""
from pytest import MonkeyPatch
import requests
from src.scraper import scrape_news
from .mock_html import MOCK_HTML

def test_scrape_news(monkeypatch: MonkeyPatch):
    """Test that mock the request and check the correct behaviour for the scraping function."""
    mock_response = type('mock', (object,), {'text': MOCK_HTML})

    def mock_get(*_, **__):
        return mock_response

    monkeypatch.setattr(requests, 'get', mock_get)

    # Get mocked news
    entries = scrape_news()

    # Check there are two entries
    assert len(entries) == 2

    # Check elements are correctly parsed
    assert entries[0]['number'] == 1
    assert entries[0]['title'] == "Show HN: Free e-book about WebGPU Programming"
    assert entries[0]['points'] == 187
    assert entries[0]['comments'] == 19

    # Check elements are correctly parsed
    assert entries[1]['number'] == 2
    assert entries[1]['title'] == "How I Program in 2024"
    assert entries[1]['points'] == 228
    assert entries[1]['comments'] == 150

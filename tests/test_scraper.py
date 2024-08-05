import requests
from src.scraper import scrape_news
from .mock_html import mock_html

def test_scrape_news(monkeypatch):
    mock_response = type('mock', (object,), {'text': mock_html})

    def mock_get(*args, **kwargs):
        return mock_response

    monkeypatch.setattr(requests, 'get', mock_get)

    entries = scrape_news()

    assert len(entries) == 2  # Assert the number of scraped entries
    assert entries[0]['title'] == "Show HN: Free e-book about WebGPU Programming"
    assert entries[1]['title'] == "How I Program in 2024"

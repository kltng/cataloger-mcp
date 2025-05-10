import pytest
from server import search_lcsh
import requests
from unittest.mock import patch

def test_search_lcsh_basic():
    # A simple test with a common subject heading
    query = "history"
    result = search_lcsh(query)
    assert isinstance(result, dict)
    assert "results" in result
    assert isinstance(result["results"], list)
    assert len(result["results"]) > 0
    for item in result["results"]:
        assert "label" in item
        assert "uri" in item
        assert isinstance(item["label"], str)
        assert isinstance(item["uri"], str)

def test_search_lcsh_no_results():
    # Query that should yield no results
    query = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    result = search_lcsh(query)
    assert isinstance(result, dict)
    assert "results" in result
    assert isinstance(result["results"], list)
    assert len(result["results"]) == 0

def test_search_lcsh_empty_query():
    # Empty query string
    query = ""
    result = search_lcsh(query)
    assert isinstance(result, dict)
    assert "results" in result or "error" in result
    # If results, should be a list
    if "results" in result:
        assert isinstance(result["results"], list)

def test_search_lcsh_invalid_api():
    # Monkeypatch requests.get to simulate a network error
    def mock_get(*args, **kwargs):
        raise requests.ConnectionError("Simulated connection error")
    with patch("requests.get", mock_get):
        result = search_lcsh("history")
        assert isinstance(result, dict)
        assert "error" in result
        assert result["type"] == "ConnectionError"

if __name__ == "__main__":
    pytest.main([__file__])

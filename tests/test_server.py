"""
Tests for the LCSH MCP Server package.
"""

import pytest
from lcsh_mcp_server.server import search_lcsh
import requests
from unittest.mock import patch


def test_search_lcsh_basic():
    """Test basic search functionality with a common subject heading."""
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
    """Test search with a query that should yield no results."""
    query = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    result = search_lcsh(query)
    assert isinstance(result, dict)
    assert "results" in result
    assert isinstance(result["results"], list)
    assert len(result["results"]) == 0


def test_search_lcsh_empty_query():
    """Test search with an empty query string."""
    query = ""
    result = search_lcsh(query)
    assert isinstance(result, dict)
    assert "results" in result or "error" in result
    # If results, should be a list
    if "results" in result:
        assert isinstance(result["results"], list)


def test_search_lcsh_invalid_api():
    """Test handling of API errors."""
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

"""
LCSH MCP Server - Core server implementation.

This module provides the MCP server functionality for searching
Library of Congress Subject Headings (LCSH).
"""

from mcp.server.fastmcp import FastMCP
import requests
import traceback

# Create the MCP server instance
mcp = FastMCP("LCSH Search Server")


@mcp.tool()
def search_lcsh(query: str) -> dict:
    """
    Search Library of Congress Subject Headings (LCSH) using the public suggest2 API.
    Returns a dictionary with the top results.
    """
    # Construct the API endpoint for LCSH subject headings
    url = "https://id.loc.gov/authorities/subjects/suggest2"
    params = {"q": query, "count": 10}
    headers = {"User-Agent": "lcsh-mcp-server/1.0 (contact: your-email@example.com)"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        # Try to parse JSON, but handle unexpected formats robustly
        try:
            data = response.json()
        except Exception as json_err:
            return {
                "error": f"Failed to parse JSON: {json_err}",
                "raw_response": response.text,
                "type": type(json_err).__name__,
                "traceback": traceback.format_exc()
            }
        # Handle new API response format (dict with 'hits')
        if isinstance(data, dict) and 'hits' in data:
            results = []
            for hit in data['hits']:
                label = hit.get('aLabel') or hit.get('label') or ''
                uri = hit.get('uri') or ''
                results.append({"label": label, "uri": uri})
            return {"results": results}
        # Old format (list with ids/labels)
        if isinstance(data, list) and len(data) >= 3:
            results = []
            for uri, label in zip(data[1], data[2]):
                results.append({"label": label, "uri": uri})
            return {"results": results}
        else:
            return {
                "error": "Unexpected API response format",
                "data": data
            }
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }


# Add resource endpoint
@mcp.resource("lcsh://search/{query}")
def lcsh_resource(query: str) -> dict:
    """Resource endpoint for LCSH search."""
    return search_lcsh(query)


def run_server(port=None):
    """
    Run the LCSH MCP server.
    
    Args:
        port (int, optional): Port number for HTTP/SSE mode. 
                             If None, runs in stdio mode.
    """
    if port is not None:
        import uvicorn
        print(f"Starting LCSH MCP server on HTTP port {port}")
        uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=port)
    else:
        # Run in stdio mode (default)
        mcp.run()

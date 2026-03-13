from mcp.server.fastmcp import FastMCP
import requests
import traceback
import time

mcp = FastMCP("cataloger mcp server")

LOC_USER_AGENT = "cataloger-mcp-server/1.0 (https://github.com/kltng/cataloger-mcp)"
LOC_HEADERS = {"User-Agent": LOC_USER_AGENT, "Accept": "application/json"}

def loc_request_with_retry(url, params, timeout=10, max_retries=2):
    """Make a LOC API request with retry on 429/503."""
    for attempt in range(max_retries + 1):
        response = requests.get(url, params=params, headers=LOC_HEADERS, timeout=timeout)
        if response.ok:
            return response
        if response.status_code in (429, 503) and attempt < max_retries:
            delay = 2 ** (attempt + 1)  # 2s, 4s
            time.sleep(delay)
            continue
        response.raise_for_status()
    return response

@ mcp.tool()
def search_lcsh(query: str) -> dict:
    """
    Search Library of Congress Subject Headings (LCSH) using the public suggest2 API.
    Returns a dictionary with the top results.
    """
    # Construct the API endpoint for LCSH subject headings
    url = "https://id.loc.gov/authorities/subjects/suggest2"
    params = {"q": query, "count": 25}
    try:
        response = loc_request_with_retry(url, params)
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

@ mcp.tool()
def search_lcsh_keyword(query: str) -> dict:
    """
    Search Library of Congress Subject Headings (LCSH) using the public suggest2 API with keyword search.
    Returns a dictionary with the top results.
    """
    # Construct the API endpoint for LCSH subject headings
    url = "https://id.loc.gov/authorities/subjects/suggest2"
    params = {"q": query, "searchtype": "keyword", "count": 50}
    try:
        response = loc_request_with_retry(url, params)
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

@mcp.tool()
def search_name_authority(query: str) -> dict:
    """
    Search Library of Congress Name Authorities (LCNAF) using the public suggest2 API.
    Specifically targets Personal Names.
    Returns a dictionary with the top results.
    """
    # Construct the API endpoint for LCNAF (Personal Names)
    url = "https://id.loc.gov/authorities/names/suggest2"
    params = {"q": query, "rdftype": "PersonalName", "count": 25}
    try:
        response = loc_request_with_retry(url, params)
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
        # Handle API response format (dict with 'hits') - primary expected format for Suggest2
        if isinstance(data, dict) and 'hits' in data:
            results = []
            for hit in data['hits']:
                label = hit.get('aLabel') or hit.get('label') or ''
                uri = hit.get('uri') or ''
                results.append({"label": label, "uri": uri})
            return {"results": results}
        # Fallback for other potential list-based formats
        elif isinstance(data, list) and len(data) > 0:
            # If it's a list of dicts (like 'hits' but without the top-level 'hits' key)
            if isinstance(data[0], dict) and ('aLabel' in data[0] or 'label' in data[0]) and 'uri' in data[0]:
                results = []
                for hit in data: # Assuming each item in the list is a hit
                    label = hit.get('aLabel') or hit.get('label') or ''
                    uri = hit.get('uri') or ''
                    results.append({"label": label, "uri": uri})
                return {"results": results}
            # If it's the [query, [labels], [uris]] structure (more like 'Suggest' API)
            elif len(data) >= 3 and isinstance(data[1], list) and isinstance(data[2], list):
                 results = []
                 # Ensure data[1] (labels) and data[2] (uris) are lists of same length
                 if len(data[1]) == len(data[2]):
                     for label_item, uri_item in zip(data[1], data[2]):
                        label = str(label_item) if label_item is not None else ''
                        uri = str(uri_item) if uri_item is not None else ''
                        results.append({"label": label, "uri": uri})
                     return {"results": results}
                 else: # Mismatched lengths in labels/URIs lists
                    return {
                        "error": "Mismatch in lengths of label and URI lists in API response",
                        "data": data
                    }
            else: # Unrecognized list format
                return {
                    "error": "Unexpected list-based API response format for name authority search",
                    "data": data
                }
        else: # Neither 'hits' dict nor a recognized list format
            return {
                "error": "Unexpected API response format for name authority search",
                "data": data
            }
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }

# Optionally, add a resource for the new tool
@mcp.resource("lcnaf://search/{query}")
def lcnaf_resource(query: str) -> dict:
    return search_name_authority(query)


# Optionally, add a resource or prompt for demonstration
@mcp.resource("lcsh://search/{query}")
def lcsh_resource(query: str) -> dict:
    return search_lcsh(query)

def start_mcp_server(port: int = None):
    """Starts the MCP server, either in HTTP/SSE mode or stdio mode."""
    import uvicorn

    if port is not None:
        # Run as HTTP/SSE server
        print(f"Starting cataloger mcp server on HTTP port {port}")
        uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=port)
    else:
        # Run in stdio mode (default)
        print("Starting cataloger mcp server in stdio mode")
        mcp.run()

if __name__ == "__main__":
    # This allows running server.py directly for testing if needed,
    # though the primary entry point is via cli.py.
    # For direct execution, it will default to stdio mode unless a port is passed as a CLI arg.
    import sys
    cli_port = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        cli_port = int(sys.argv[1])
    start_mcp_server(port=cli_port)

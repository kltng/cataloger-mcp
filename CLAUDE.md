# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **cataloger-mcp-server**, a Model Context Protocol (MCP) server that provides access to Library of Congress Subject Headings (LCSH) and Name Authorities (LCNAF) through a simple API interface. It allows AI assistants to search authoritative library cataloging data using the public suggest2 API.

## Development Commands

### Installation and Setup
```bash
# Install in development mode
pip install -e .

# Install dependencies using uv (preferred)
uv pip install -e .

# Or install from PyPI
pip install cataloger-mcp-server
```

### Running the Server
```bash
# Run in stdio mode (default, for Claude Desktop integration)
cataloger-mcp-server

# Run with explicit CLI module
python -m cataloger_mcp_server.cli

# Run in HTTP/SSE mode on port 6274 (for testing/debugging)
cataloger-mcp-server --port 6274
```

### Testing
```bash
# Run all tests
python -m pytest test_server.py -v

# Run specific test
python -m pytest test_server.py::test_search_lcsh_basic -v

# Run tests with coverage (if installed)
python -m pytest --cov=cataloger_mcp_server test_server.py
```

### Testing with MCP Inspector
```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Start server in HTTP mode first
cataloger-mcp-server --port 6274

# Test with inspector (in separate terminal)
npx @modelcontextprotocol/inspector http://localhost:6274
```

## Architecture

### Core Components

- **`src/cataloger_mcp_server/server.py`** - Main MCP server implementation using FastMCP
- **`src/cataloger_mcp_server/cli.py`** - Command-line interface entry point
- **`test_server.py`** - pytest test suite (root level, not in tests/ directory)

### MCP Tools Available

1. **`search_lcsh(query)`** - Left-anchored search in LCSH (default search type)
2. **`search_lcsh_keyword(query)`** - Keyword search in LCSH (more flexible matching)
3. **`search_name_authority(query)`** - Search LCNAF for Personal Names

### Resource Endpoints

- **`lcsh://search/{query}`** - Resource endpoint for LCSH searches
- **`lcnaf://search/{query}`** - Resource endpoint for LCNAF searches

### API Integration

The server integrates with Library of Congress APIs:
- **LCSH API**: `https://id.loc.gov/authorities/subjects/suggest2`
- **LCNAF API**: `https://id.loc.gov/authorities/names/suggest2`

Key response formats handled:
- **New format**: Dictionary with `hits` array containing objects with `aLabel`/`label` and `uri` fields
- **Legacy format**: Array structure `[query, [labels], [uris]]`

### Error Handling Strategy

The server implements robust error handling with consistent response format:
```python
{
    "error": "Error description",
    "type": "ErrorType",
    "traceback": "Full traceback for debugging"
}
```

### Operation Modes

1. **stdio mode** - For direct integration with AI assistants (default)
2. **HTTP/SSE mode** - For network-based connections on specified port

## Development Guidelines

### Code Organization

- Use FastMCP decorators (`@mcp.tool()`, `@mcp.resource()`) for exposing functionality
- Implement comprehensive error handling with try/catch blocks
- Return consistent response formats across all tools
- Include timeout handling (10 seconds) for external API calls

### Testing Approach

- Test both success and failure scenarios
- Mock external API calls for error condition testing
- Test edge cases like empty queries and malformed responses
- Validate response structure and data types

### API Response Parsing

The codebase handles multiple API response formats defensively:
- Always check if response is dict with `hits` key first
- Fall back to legacy list format handling
- Validate expected field existence with fallbacks
- Handle missing or null label/URI values gracefully

## Dependencies

Core dependencies managed in `pyproject.toml`:
- `mcp[cli]>=1.6.0` - MCP Python SDK with CLI tools
- `requests>=2.32.3` - HTTP client for API calls
- `uvicorn>=0.27.0` - ASGI server for HTTP mode
- `click==8.3.0` - CLI framework
- FastMCP (from mcp package) - MCP server framework

## Project Structure Notes

- Source code in `src/cataloger_mcp_server/` following modern Python packaging
- Tests at root level (`test_server.py`) rather than in `tests/` directory
- Entry point defined as `cataloger-mcp-server = "cataloger_mcp_server.cli:main"`
- Uses hatchling build system with wheel packages only
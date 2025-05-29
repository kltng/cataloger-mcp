# cataloger mcp server

A Model Context Protocol (MCP) server that provides access to the Library of Congress Subject Headings (LCSH) through a simple API interface.

## Overview

This MCP server allows AI assistants to search the Library of Congress Subject Headings (LCSH) using the public suggest2 API. It provides a clean interface for querying LCSH data and handling the various response formats from the API.

## Features

- **MCP Tool Integration**: Exposes a `search_lcsh` tool that can be used by AI assistants
- **Resource Endpoint**: Provides a resource endpoint at `lcsh://search/{query}`
- **Robust Error Handling**: Gracefully handles API errors, connection issues, and unexpected response formats
- **Multiple Response Formats**: Supports both dictionary (hits) and list response formats from the LCSH API
- **Dual Operation Modes**: 
  - **stdio mode**: For direct integration with AI assistants like Claude Desktop
  - **HTTP/SSE mode**: For network-based connections on a specified port

## Requirements

- Python 3.12 or higher
- Dependencies:
  - `mcp[cli]>=1.6.0`: Model Context Protocol Python SDK
  - `requests>=2.32.3`: HTTP library for API requests

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd lcsh-mcp

# Set up a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies using uv
uv pip install -e .
```

## Usage

### Running in stdio Mode (Default)

This mode is ideal for direct integration with AI assistants like Claude Desktop:

```bash
python server.py
```

### Running in HTTP/SSE Mode

This mode allows network-based connections on the specified port:

```bash
python server.py 6274
```

The server will start on port 6274 (or any port you specify) and be accessible at `http://localhost:6274`.

## API Reference

### Tool: `search_lcsh`

Searches the Library of Congress Subject Headings using the public suggest2 API.

**Parameters:**
- `query` (string): The search term to look for in LCSH

**Returns:**
A dictionary with the following structure:

```json
{
  "results": [
    {
      "label": "Subject Heading Label",
      "uri": "http://id.loc.gov/authorities/subjects/..."
    },
    ...
  ]
}
```

Or in case of an error:

```json
{
  "error": "Error message",
  "type": "ErrorType",
  "traceback": "..."
}
```

### Resource: `lcsh://search/{query}`

A resource endpoint that returns the same data as the `search_lcsh` tool.

## Testing

The server includes a comprehensive test suite that can be run with pytest:

```bash
python -m pytest test_server.py -v
```

Tests cover basic functionality, empty queries, no results, and API errors.

## Integration with Claude Desktop

To use this MCP server with Claude Desktop:

1. Start the server in stdio mode: `python server.py`
2. In Claude Desktop, go to Settings > MCP Servers
3. Add a new MCP server with the following configuration:
   - Name: cataloger mcp Search
   - Command: `python /path/to/cataloger mcp/server.py`
4. Enable the server and start using the cataloger mcp search capabilities in your conversations

## License

[Specify your license here]

## Contributing

[Add contribution guidelines if applicable]

## Testing with MCP Inspector

The MCP Inspector is a visual testing tool specifically designed for MCP servers. Here's how to use it with your cataloger mcp server:

### Step 1: Install MCP Inspector

First, you need to install the MCP Inspector. You can use npm to install it globally:

```bash
npm install -g @modelcontextprotocol/inspector
```

Or you can use it directly with npx without installing:

```bash
npx @modelcontextprotocol/inspector
```

### Step 2: Start Your cataloger mcp server

You need to have your cataloger mcp server running in HTTP/SSE mode for testing with the Inspector:

```bash
python server.py 6274
```

This will start your server on port 6274 (or you can choose another port).

### Step 3: Connect MCP Inspector to Your Server

Now you can connect the MCP Inspector to your running server. There are two ways to do this:

#### Option 1: Using the CLI

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:6274
```

This will connect to your server in CLI mode and allow you to interact with it through the command line.

#### Option 2: Using the Web Interface

```bash
npx @modelcontextprotocol/inspector
```

This will start the MCP Inspector web interface. By default, it runs on port 3000, so you can access it at http://localhost:3000 in your browser. Once the interface loads:

1. Click on "Add Server"
2. Enter a name for your server (e.g., "cataloger mcp server")
3. Enter the URL: `http://localhost:6274`
4. Click "Save"

### Step 4: Test Your Server's Tools and Resources

Once connected, you can:

#### List Available Tools

CLI:
```bash
npx @modelcontextprotocol/inspector --cli http://localhost:6274 --method tools/list
```

Web Interface:
- Click on your server in the sidebar
- Go to the "Tools" tab to see all available tools

#### Test the `search_lcsh` Tool

CLI:
```bash
npx @modelcontextprotocol/inspector --cli http://localhost:6274 --method tools/call --tool-name search_lcsh --tool-arg query=history
```

Web Interface:
- Click on the "search_lcsh" tool
- Enter "history" (or any search term) in the query field
- Click "Execute"
- View the results in the response panel

#### Test the Resource Endpoint

CLI:
```bash
npx @modelcontextprotocol/inspector --cli http://localhost:6274 --method resources/list
```

Web Interface:
- Go to the "Resources" tab
- You should see the `lcsh://search/{query}` resource
- You can test it by entering a query parameter

### Step 5: Debugging and Monitoring

The MCP Inspector provides detailed information about:

- Request and response payloads
- Execution times
- Any errors that occur

This makes it an excellent tool for debugging your MCP server and ensuring it's working correctly.

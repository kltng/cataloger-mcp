# cataloger mcp server

A Model Context Protocol (MCP) server that provides access to the Library of Congress Subject Headings (LCSH) through a simple API interface.

## Overview

This MCP server allows AI assistants like Claude to search the Library of Congress Subject Headings (LCSH) using the public suggest2 API. It provides a clean interface for querying LCSH data and handling the various response formats from the API.

## Installation

### Option 1: Install from PyPI (Recommended)

The easiest way to install the cataloger mcp server is directly from PyPI:

```bash
pip install cataloger-mcp-server
```

### Option 2: Install from Source

If you prefer to install from source:

```bash
git clone https://github.com/kltng/cataloger-mcp-server.git
cd cataloger-mcp-server
pip install -e .
```

## Setting up with Claude Desktop

1. **Install Claude Desktop** if you haven't already from [https://claude.ai/desktop](https://claude.ai/desktop)

2. **Install the cataloger mcp server** using one of the installation methods above

3. **Open Claude Desktop** and navigate to Settings:
   - Click on your profile picture in the bottom-left corner
   - Select "Settings" from the menu

4. **Configure the MCP Server**:
   - In the Settings panel, click on "MCP Servers"
   - Click "Add Server"
   - Fill in the following details:
     - **Name**: `cataloger mcp search`
     - **Command**: `cataloger-mcp-server`
   - Click "Save"

5. **Enable the Server**:
   - Toggle the switch next to the cataloger mcp search server to enable it
   - Claude will now have access to the LCSH search capabilities

## Using the cataloger mcp server with Claude

Once the server is set up and enabled in Claude Desktop, you can ask Claude to search for Library of Congress Subject Headings. Here are some example prompts:

- "Can you search the Library of Congress Subject Headings for 'artificial intelligence'?"
- "Look up 'climate change' in LCSH and tell me the official subject headings."
- "What are the LCSH terms related to 'quantum computing'?"

Claude will use the MCP server to query the LCSH and LCNAF databases and return the results.

- "Find the name authority record for 'Smith, John Adam'."
- "Perform a keyword search in LCSH for 'environmental policy'.

## Features

- **MCP Tool Integration**: Exposes `search_lcsh` (for subject headings, default left-anchored search), `search_lcsh_keyword` (for subject headings, keyword search), and `search_name_authority` (for personal names) tools that can be used by AI assistants.
- **Resource Endpoints**: Provides resource endpoints at `lcsh://search/{query}` and `lcnaf://search/{query}`.
- **Robust Error Handling**: Gracefully handles API errors, connection issues, and unexpected response formats
- **Multiple Response Formats**: Supports both dictionary (hits) and list response formats from the LCSH API

## Troubleshooting

If you encounter issues with the MCP server:

1. **Check Server Status**: In Claude Desktop, go to Settings > MCP Servers and check if the server is enabled and running
2. **Restart the Server**: Toggle the server off and on again
3. **Check Console Output**: If running the server manually, check the console output for any error messages
4. **Verify Network Connection**: Ensure your computer has an active internet connection to access the LCSH API

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## For Developers

For more detailed documentation about the server implementation, API references, and testing information, please refer to the [references.md](references.md) file.

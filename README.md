# LCSH MCP Server

A Model Context Protocol (MCP) server that provides access to the Library of Congress Subject Headings (LCSH) through a simple API interface.

## Overview

This MCP server allows AI assistants like Claude to search the Library of Congress Subject Headings (LCSH) using the public suggest2 API. It provides a clean interface for querying LCSH data and handling the various response formats from the API.

## Installation

### Option 1: Install from PyPI (Recommended)

The easiest way to install the LCSH MCP server is directly from PyPI:

```bash
pip install lcsh-mcp-server
```

### Option 2: Install from Source

If you prefer to install from source:

```bash
git clone https://github.com/kltng/lcsh-mcp-server.git
cd lcsh-mcp-server
pip install -e .
```

## Setting up with Claude Desktop

1. **Install Claude Desktop** if you haven't already from [https://claude.ai/desktop](https://claude.ai/desktop)

2. **Install the LCSH MCP Server** using one of the installation methods above

3. **Open Claude Desktop** and navigate to Settings:
   - Click on your profile picture in the bottom-left corner
   - Select "Settings" from the menu

4. **Configure the MCP Server**:
   - In the Settings panel, click on "MCP Servers"
   - Click "Add Server"
   - Fill in the following details:
     - **Name**: `LCSH Search`
     - **Command**: `lcsh-mcp-server`
   - Click "Save"

5. **Enable the Server**:
   - Toggle the switch next to the LCSH Search server to enable it
   - Claude will now have access to the LCSH search capabilities

## Using the LCSH MCP Server with Claude

Once the server is set up and enabled in Claude Desktop, you can ask Claude to search for Library of Congress Subject Headings. Here are some example prompts:

- "Can you search the Library of Congress Subject Headings for 'artificial intelligence'?"
- "Look up 'climate change' in LCSH and tell me the official subject headings."
- "What are the LCSH terms related to 'quantum computing'?"

Claude will use the MCP server to query the LCSH database and return the results.

## Features

- **MCP Tool Integration**: Exposes a `search_lcsh` tool that can be used by AI assistants
- **Resource Endpoint**: Provides a resource endpoint at `lcsh://search/{query}`
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

## Using the cataloger MCP Server with Cherry Studio

This tutorial walks you through, in detail, how to install Cherry Studio, configure it to use the **cataloger-mcp-server** via the Model Context Protocol (MCP), and verify that everything is working. It assumes no prior experience with MCP.

---

## 1. What you will set up

By the end of this tutorial you will have:

- Cherry Studio installed on your machine.
- The **cataloger-mcp-server** configured as an MCP server inside Cherry Studio.
- A working JSON configuration using:

  ```json
  {
    "mcpServers": {
      "cataloger-mcp": {
        "command": "uvx",
        "args": ["cataloger-mcp-server"]
      }
    }
  }
  ```

- A verified workflow where Cherry Studio can:
  - Call the MCP server.
  - Search Library of Congress Subject Headings (LCSH).
  - Use name authority lookup for personal names (LCNAF).

---

## 2. Prerequisites

Before you start, you should have:

- A computer running a supported desktop OS (Windows, macOS, or a supported Linux).
- Internet access (needed for:
  - downloading Cherry Studio,
  - `uvx` to resolve the `cataloger-mcp-server` package,
  - and for the MCP server to contact the Library of Congress APIs).
- Basic comfort with opening a terminal / command prompt when needed.

You do **not** need deep Python or MCP knowledge to follow this tutorial.

---

## 3. Install Cherry Studio

1. Open your web browser and go to the Cherry documentation / download page:  
   - <https://docs.cherry-ai.com/docs/en-us/advanced-basic/mcp/install>  
   - or the main site: <https://docs.cherry-ai.com/advanced-basic/mcp>

2. Download the installer for your platform:
   - **Windows**: `.exe` installer.
   - **macOS**: `.dmg` or `.pkg` installer.
   - **Linux**: follow the instructions provided on the Cherry site (AppImage, package manager, or other method).

3. Run the installer:
   - **Windows**: double-click the `.exe`, follow the wizard, and allow it to create a desktop/start menu shortcut.
   - **macOS**: open the `.dmg` and drag Cherry Studio to `Applications` (or follow the `.pkg` installer instructions).
   - **Linux**: follow the distribution-specific instructions from Cherry.

4. Once installation completes, start Cherry Studio:
   - Use the newly created application icon / shortcut.
   - Wait for the app to fully load.

5. If prompted, sign in or complete any initial onboarding as required by the Cherry version you are using.

You now have Cherry Studio installed and running.

---

## 4. Install or verify `uv` / `uvx`

In the recommended configuration, Cherry Studio will use the `uvx` command to run the MCP server:

```json
{
  "mcpServers": {
    "cataloger-mcp": {
      "command": "uvx",
      "args": ["cataloger-mcp-server"]
    }
  }
}
```

This means:

- `uvx` will automatically download and run the `cataloger-mcp-server` package if it is not already installed.
- You do not strictly need to install `cataloger-mcp-server` manually, but you **must** have `uv` installed and on your `PATH`.

### 4.1 Install `uv`

Follow the official `uv` install instructions (see <https://docs.astral.sh/uv/>), which typically look like:

- **macOS / Linux** (shell):

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **Windows (PowerShell)**:

  ```powershell
  irm https://astral.sh/uv/install.ps1 | iex
  ```

After installation, restart your terminal or log out and back in if needed so that `uv` and `uvx` are available on your `PATH`.

### 4.2 Verify `uvx` is available

Open a terminal / command prompt and run:

```bash
uvx --version
```

You should see a version string (for example: `uvx 0.4.x`). If you get “command not found” or similar, verify you completed the installation steps and that your shell is configured to find `uv`.

---

## 5. (Optional) Install `cataloger-mcp-server` manually

Because `uvx` can resolve packages on demand, you do not need to pre-install `cataloger-mcp-server`. However, installing it manually can make first startup a bit faster and helps with local development or testing.

You have two common options:

### 5.1 Install from PyPI with `pip`

```bash
pip install cataloger-mcp-server
```

### 5.2 Install in development mode from source

If you have cloned this repository:

```bash
cd path/to/cataloger-mcp
pip install -e .
```

or, using `uv`:

```bash
uv pip install -e .
```

Once installed, you can manually test the server by running:

```bash
cataloger-mcp-server
```

You should see logging that indicates the MCP server is running (by default, in stdio mode).

---

## 6. Configure the MCP server in Cherry Studio (JSON import)

Cherry Studio supports configuring MCP servers using a JSON definition. In this tutorial, you will use the **Import JSON** method.

### 6.1 Prepare the JSON snippet

Create a JSON snippet exactly like this (you will paste it into Cherry Studio in a later step):

```json
{
  "mcpServers": {
    "cataloger-mcp": {
      "command": "uvx",
      "args": ["cataloger-mcp-server"]
    }
  }
}
```

Notes:

- The outermost object has a single key: `"mcpServers"`.
- The key `"cataloger-mcp"` is the **identifier** Cherry Studio will show for this MCP server. You may change this label if you like (for example `"lcsh-cataloger"`), but keep the internal structure the same.
- JSON does **not** allow comments or trailing commas. Make sure the snippet is copied exactly as shown.

### 6.2 Open the MCP configuration screen

1. With Cherry Studio running, open the settings/preferences:
   - Look for a gear icon, `Settings` menu, or similar (exact wording may vary by version).
   - Navigate to the **MCP** or **MCP Servers** section, as described in the Cherry documentation.

2. Look for an option labeled something like:
   - `Add`
   - `Import from JSON`
   - or `Import MCP configuration`

   The exact label may vary slightly between Cherry Studio versions, but it will be in the MCP configuration area.

### 6.3 Import the JSON

1. Click the **Import from JSON** (or equivalent) button.
2. A dialog or text input area should appear where you can paste JSON.
3. Paste the JSON snippet:

   ```json
   {
     "mcpServers": {
       "cataloger-mcp": {
         "command": "uvx",
         "args": ["cataloger-mcp-server"]
       }
     }
   }
   ```

4. Confirm or save:
   - Click **OK**, **Save**, or **Import** (depending on the UI) to apply the configuration.

If the JSON is valid, Cherry Studio will add a new MCP server entry named `cataloger-mcp` (or whatever key you chose).

---

## 7. Verify the MCP server entry in Cherry Studio

After importing the JSON:

1. Stay in the MCP/MCP Servers section of Cherry Studio’s settings.
2. Locate the newly created entry (for example, `cataloger-mcp`).
3. Confirm the configuration fields:
   - **Name/ID**: `cataloger-mcp`
   - **Command**: `uvx`
   - **Arguments**: `["cataloger-mcp-server"]` (displayed according to how Cherry shows arrays/arguments)

4. Ensure the server is **enabled**:
   - Most MCP UIs expose a toggle or checkbox to enable/disable a server.
   - Turn it **on**.

5. Cherry Studio may attempt to start the MCP server immediately; if so, you might see:
   - A running status indicator.
   - Log output or a small indicator that the MCP server is connected.

If you see an error (for example, “command not found: uvx” or “cataloger-mcp-server not found”), refer to the troubleshooting section below.

---

## 8. Start a new chat and test the MCP

Now that the MCP server is configured and enabled, test it from a conversation.

1. Open Cherry Studio’s main chat interface.
2. Start a new conversation:
   - Click `New Chat` or equivalent.

3. Make sure the conversation is allowed to use MCP tools:
   - Some UIs have a per-conversation configuration listing which MCP servers are available.
   - Confirm that the `cataloger-mcp` server is enabled / selected for this chat if Cherry presents such controls.

4. Send a prompt that clearly requires LCSH or authority searching, such as:

   - “Use the cataloger MCP tools to find Library of Congress Subject Headings for a book about climate change policy in the United States.”
   - “Search LCSH for subject headings related to ‘quantum computing’.”
   - “Find established LCSH terms related to Renaissance art and patronage.”

5. Observe the behavior:
   - Cherry Studio should call the MCP server in the background.
   - The model’s response should include headings or explanations clearly derived from LCSH / LCNAF.

If Cherry exposes a “Tools” or “Requests” panel, you may see:

- A call to `search_lcsh` or `search_lcsh_keyword` with your query.
- Responses from the MCP server that include LCSH labels and URIs.

---

## 9. Example MCP usage patterns with this server

Once everything is working, here are some concrete example prompts you can use to exercise the MCP server.

### 9.1 Basic topical LCSH search

Prompt:

> Use the cataloger MCP server to find established LCSH headings for a monograph about climate change policy in the United States, focusing on government regulation and environmental law.

Expected behavior:

- The model should:
  - Identify candidate topical headings (for example, `Climatic changes--Government policy--United States`, depending on LCSH).
  - Use `search_lcsh` to validate those candidate headings.
  - Possibly use `search_lcsh_keyword` with queries like `"climate change AND policy AND United States"` to discover related or more specific headings.

### 9.2 Keyword-based discovery

Prompt:

> The work is about urban redevelopment and gentrification in 21st-century New York City. Use keyword searches via the cataloger MCP to find the most appropriate LCSH headings, and then propose a small set of 3–5 headings.

Expected behavior:

- The model should:
  - Identify keywords like `urban renewal`, `gentrification`, `New York (N.Y.)`, `21st century`.
  - Send queries to `search_lcsh_keyword` such as `"gentrification AND New York"` or `"urban renewal AND New York City"`.
  - Use the returned LCSH terms to build its final recommendation list.

### 9.3 Personal name as subject (LCNAF)

Prompt:

> This biography is about the physicist Richard Feynman. Use the cataloger MCP tools to look up the established name heading for him and any suitable subject headings about his work and influence.

Expected behavior:

- The model should:
  - Use `search_name_authority` with a query such as `"Feynman, Richard P."`.
  - Return the established LCNAF form and URI for Feynman.
  - Use `search_lcsh` and/or `search_lcsh_keyword` for related topical headings (for example, quantum electrodynamics, physics—History, etc.).

---

## 10. Alternative configuration: direct command without `uvx`

If you prefer not to use `uvx`, and you have installed `cataloger-mcp-server` with `pip` so that the `cataloger-mcp-server` command is directly available on your `PATH`, you can use this alternative JSON:

```json
{
  "mcpServers": {
    "cataloger-mcp": {
      "command": "cataloger-mcp-server",
      "args": []
    }
  }
}
```

In this case:

- Cherry Studio will call `cataloger-mcp-server` directly.
- You remain responsible for keeping the package updated via `pip` or your chosen package manager.

The rest of the Cherry Studio configuration steps (importing JSON, enabling the server, and testing) remain the same.

---

## 11. Troubleshooting

If something does not work as expected, here are common issues and how to diagnose them.

### 11.1 Cherry Studio says “command not found: uvx”

Symptoms:

- The MCP server entry shows an error.
- The logs or error panel mention `uvx: command not found` or similar.

Check:

1. Open a terminal and run:

   ```bash
   uvx --version
   ```

2. If this fails:
   - Reinstall `uv` using the instructions from section 4.
   - Make sure your shell environment is reloaded so that `uvx` is on `PATH`.

3. If the command works in the terminal but not from Cherry Studio:
   - Cherry Studio may be using a different environment (for example, a different user account or shell).
   - Try fully quitting and restarting Cherry Studio after installing `uv`.

### 11.2 Cherry Studio says “cataloger-mcp-server not found”

If you are using the **direct command** configuration (without `uvx`):

1. Run:

   ```bash
   cataloger-mcp-server --help
   ```

2. If this fails:
   - Install the package:

     ```bash
     pip install cataloger-mcp-server
     ```

   - Or ensure that the appropriate `Scripts` or `bin` directory is on your `PATH`.

If you are using the **`uvx` configuration**:

- Normally `uvx` will fetch and run the package on demand.
- If there is a network or configuration issue, you may see error messages in:
  - Cherry Studio’s MCP log area.
  - Or in the console if Cherry Studio exposes MCP logs.

### 11.3 The MCP server starts, but no LCSH results appear

If the MCP server appears to be running, but you do not see any LCSH-related results:

1. Make sure your prompts explicitly ask the model to use the **cataloger MCP** or to perform LCSH / authority searches.
2. Check whether the model/tool-usage view shows calls to:
   - `search_lcsh`
   - `search_lcsh_keyword`
   - `search_name_authority`
3. If no such calls appear:
   - Ensure the MCP server is **enabled** in Cherry Studio for that conversation.
   - Try prompting more explicitly, for example:

     > Use the cataloger MCP tools to search LCSH and show me the headings you retrieved, including their URIs.

4. If calls appear but the results seem empty or error-prone:
   - Check your network connection (the MCP server queries Library of Congress APIs).
   - Look at any error messages returned by the server in the log.

### 11.4 JSON import fails

If Cherry Studio rejects your JSON:

1. Double-check that the snippet is **exact JSON**, with:
   - Double quotes around all keys and string values.
   - No trailing commas.
   - Proper curly brace and bracket pairing.
2. Compare your snippet to this known-good template:

   ```json
   {
     "mcpServers": {
       "cataloger-mcp": {
         "command": "uvx",
         "args": ["cataloger-mcp-server"]
       }
     }
   }
   ```

3. Try pasting directly from the README or this tutorial to avoid typos.

---

## 12. Summary

To recap, using the cataloger MCP server with Cherry Studio involves:

- Installing Cherry Studio.
- Installing and verifying `uv` / `uvx`.
- Importing a minimal MCP JSON configuration that defines the `cataloger-mcp` server using:

  ```json
  {
    "mcpServers": {
      "cataloger-mcp": {
        "command": "uvx",
        "args": ["cataloger-mcp-server"]
      }
    }
  }
  ```

- Enabling the server in Cherry Studio’s MCP settings.
- Starting a chat and prompting the model to use the cataloger MCP tools for LCSH and name authority work.

Once configured, Cherry Studio can leverage the cataloger-mcp-server to search and validate Library of Congress Subject Headings and name authorities directly within your cataloging workflows.


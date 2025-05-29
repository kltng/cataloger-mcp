#!/usr/bin/env python
"""
Development entry point for cataloger mcp server.
This script allows you to run the server directly during development.
"""

import sys
from src.cataloger_mcp_server.cli import main

if __name__ == "__main__":
    sys.exit(main())

"""
Command-line interface for cataloger mcp server.

This module provides the entry point for the command-line interface.
"""

import sys
import argparse
from .server import run_server


def main():
    """Main entry point for the cataloger mcp server CLI."""
    parser = argparse.ArgumentParser(
        description="cataloger mcp server - A Model Context Protocol server for "
                    "Library of Congress Subject Headings"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        help="Port number for HTTP/SSE mode. If not provided, runs in stdio mode."
    )
    
    args = parser.parse_args()
    
    # Run the server with the provided port (or None for stdio mode)
    run_server(args.port)


if __name__ == "__main__":
    sys.exit(main())

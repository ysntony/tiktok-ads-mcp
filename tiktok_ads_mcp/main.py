#!/usr/bin/env python3
"""CLI entry point for TikTok Ads FastMCP Server"""

import sys
from .server import main as run_server

def cli():
    """
    This is the command-line entry point for the TikTok Ads MCP server.
    It simply calls the main function from the server module.
    """
    try:
        run_server()
    except KeyboardInterrupt:
        print("Server shut down by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Server failed to start: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    cli()

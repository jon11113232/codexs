# Codexs

Test repository for OpenAI Codex API

## MCP Server Installation on macOS

This repository now includes a script for setting up the Computer Control MCP server in a clean Python 3.11 environment on macOS. The script resolves common dependency conflicts and ensures OCR components are installed correctly.

### Steps

1. Clone this repository.
2. Run `./install_mcp_server_mac.sh` from the project root.
   - The script creates a `mcp_env` virtual environment.
   - Required packages (`computer-control-mcp` and RapidOCR dependencies) are installed with pinned versions.
   - A short Python check confirms that `VisRes` imports successfully from `rapidocr_paddle`.
3. Activate the environment with `source mcp_env/bin/activate` and start the MCP server as documented in the package.

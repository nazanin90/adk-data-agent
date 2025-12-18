#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Setting up Python virtual environment using uv ---"

# Check if uv is installed
if ! command -v uv &> /dev/null
then
    echo "Error: uv is not installed."
    echo "Please install uv first. See https://github.com/astral-sh/uv#installation"
    echo "Common methods:"
    echo "  pip install uv"
    echo "  pipx install uv"
    exit 1
fi

# Store the uv command path before venv activation
UV_CMD=$(which uv)

# Create the virtual environment (default: .venv)
echo "Creating virtual environment..."
$UV_CMD venv

# Install dependencies including development extras
echo "Installing dependencies (including dev extras) from pyproject.toml..."
# Note: uv pip install .[dev] looks for pyproject.toml in the current directory
$UV_CMD pip install .[dev]

echo ""
echo "--- Setup complete! ---"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo "(On Windows Cmd: .venv\Scripts\activate.bat | PowerShell: .venv\Scripts\Activate.ps1)"
echo ""
echo "After activation, to run your agent locally:"
echo "  cd src/"
echo "  adk web"
echo ""

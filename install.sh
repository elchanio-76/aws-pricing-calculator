#!/bin/bash
# Installation script for AWS Pricing Calculator MCP Server

set -e

echo "AWS Pricing Calculator MCP Server - Installation"
echo "================================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "❌ Error: Python 3.10 or higher is required"
    echo "   Found: Python $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Check curl
echo "Checking for curl..."
if ! command -v curl &> /dev/null; then
    echo "❌ Error: curl is required but not found"
    echo "   Install curl: sudo apt-get install curl (Ubuntu/Debian)"
    echo "                 sudo yum install curl (RHEL/CentOS)"
    exit 1
fi

echo "✅ curl detected"
echo ""

# Install MCP package
echo "Installing MCP package..."
pip install mcp

echo "✅ MCP package installed"
echo ""

# Install the server in development mode
echo "Installing AWS Pricing Calculator MCP server..."
pip install -e .

echo "✅ MCP server installed"
echo ""

# Test the server
echo "Testing MCP server..."
if python3 -c "from mcp_server import server, tools" 2>/dev/null; then
    echo "✅ MCP server imports successfully"
else
    echo "❌ Error: MCP server failed to import"
    exit 1
fi

echo ""
echo "================================================="
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Add this power to Kiro via the Powers UI"
echo "2. The MCP server will start automatically when needed"
echo ""
echo "To test manually:"
echo "  python3 test_mcp_server.py"
echo ""

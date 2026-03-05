# AWS Pricing Calculator MCP Server Guide

## What We Built

We've converted the AWS Pricing Calculator power from CLI scripts to a proper MCP server with tools.

## Structure

```
aws-pricing-calculator/
├── mcp_server/
│   ├── __init__.py           # Package init
│   ├── server.py             # MCP server entry point
│   └── tools.py              # Tool implementations (wraps scripts)
├── scripts/                  # Original Python scripts (unchanged)
│   ├── calc_utils.py
│   ├── calc_discover.py
│   ├── calc_build.py
│   └── calc_save.py
├── steering/                 # Documentation files
│   ├── api_endpoints.md
│   ├── service_formats.md
│   └── troubleshooting.md
├── POWER.md                  # Power documentation (updated for MCP)
├── mcp.json                  # MCP server configuration
├── pyproject.toml            # Python package configuration
├── install.sh                # Installation script
└── test_mcp_server.py        # Test script
```

## MCP Tools Provided

### 1. discover_services
- **Purpose:** Fetch service schemas from AWS Pricing Calculator
- **Input:** `service_codes` (optional array)
- **Output:** Service schemas with versions and components

### 2. build_estimate
- **Purpose:** Build complete estimate JSON from specification
- **Input:** `spec` object with groups and services
- **Output:** Complete estimate JSON with totals

### 3. save_estimate
- **Purpose:** Save estimate to AWS and get shareable URL
- **Input:** `estimate` object (from build_estimate)
- **Output:** Calculator URL and summary

### 4. get_region_name
- **Purpose:** Convert region codes to display names
- **Input:** `region_code` string
- **Output:** Display name

## Installation for Users

### Option 1: Automatic (Recommended)

```bash
cd <power-install-path>
./install.sh
```

### Option 2: Manual

```bash
cd <power-install-path>
pip install mcp
pip install -e .
```

## Testing

### Test the MCP server directly:

```bash
python3 test_mcp_server.py
```

Expected output:
- ✅ List all services (430+ services)
- ✅ Discover EC2 service schema
- ✅ Get region name
- ✅ Build simple estimate

### Test in Kiro:

1. Open Powers UI in Kiro
2. Add Custom Power → Local Directory
3. Point to this directory
4. Try activating: "activate aws-pricing-calculator"
5. Test with: "List all AWS services available in the pricing calculator"

## How It Works

1. **User installs power** → Kiro reads POWER.md and mcp.json
2. **User triggers power** → Kiro starts MCP server via `python3 -m mcp_server.server`
3. **Agent calls tools** → MCP server executes tool functions
4. **Tools wrap scripts** → Original Python scripts do the actual work
5. **Results returned** → Agent receives structured JSON responses

## Key Files

### mcp.json
Tells Kiro how to start the MCP server:
```json
{
  "mcpServers": {
    "aws-pricing-calculator": {
      "command": "python3",
      "args": ["-m", "mcp_server.server"]
    }
  }
}
```

### mcp_server/server.py
- Defines MCP tools with schemas
- Handles tool calls
- Returns structured responses

### mcp_server/tools.py
- Wraps original scripts as async functions
- Provides clean interfaces for MCP
- Handles errors gracefully

## Advantages Over CLI Scripts

1. **Structured I/O:** Tools have defined input/output schemas
2. **Better Integration:** Native Kiro MCP support
3. **Error Handling:** Consistent error responses
4. **Type Safety:** Parameter validation built-in
5. **Cleaner UX:** Agents call tools instead of bash commands

## Troubleshooting

### "Module not found: mcp"
```bash
pip install mcp
```

### "Module not found: mcp_server"
```bash
pip install -e .
```

### "Python version too old"
Requires Python 3.10+. Check with:
```bash
python3 --version
```

### "curl not found"
Install curl:
```bash
# Ubuntu/Debian
sudo apt-get install curl

# RHEL/CentOS
sudo yum install curl

# macOS
brew install curl
```

## Next Steps

1. ✅ MCP server created and tested
2. ✅ POWER.md updated with MCP tool documentation
3. ✅ mcp.json configuration created
4. ✅ Installation script created
5. ⏭️ Test in Kiro Powers UI
6. ⏭️ Create GitHub repository for distribution
7. ⏭️ Submit to Kiro recommended powers (optional)

# Deployment Guide: AWS Pricing Calculator Power + MCP Server

This guide explains how to deploy the AWS Pricing Calculator as two separate repositories.

## Architecture

```
┌─────────────────────────────────────┐
│  Kiro Power Repository              │
│  (aws-pricing-calculator-power)     │
│                                     │
│  - POWER.md                         │
│  - mcp.json                         │
│  - steering/                        │
│    ├── api_endpoints.md             │
│    ├── service_formats.md           │
│    └── troubleshooting.md           │
└─────────────────────────────────────┘
                 │
                 │ references via uvx
                 ▼
┌─────────────────────────────────────┐
│  MCP Server Repository              │
│  (aws-pricing-calculator-mcp)       │
│                                     │
│  - mcp_server/                      │
│    ├── server.py                    │
│    └── tools.py                     │
│  - scripts/                         │
│    ├── calc_utils.py                │
│    ├── calc_discover.py             │
│    ├── calc_build.py                │
│    └── calc_save.py                 │
│  - pyproject.toml                   │
│  - README.md                        │
└─────────────────────────────────────┘
```

## Step 1: Create MCP Server Repository

### Files to Include

```
aws-pricing-calculator-mcp/
├── mcp_server/
│   ├── __init__.py
│   ├── server.py
│   └── tools.py
├── scripts/
│   ├── calc_utils.py
│   ├── calc_discover.py
│   ├── calc_build.py
│   └── calc_save.py
├── pyproject.toml
├── README.md (use MCP_SERVER_README.md)
├── test_mcp_server.py
├── test_mcp_stdio.py
└── .gitignore
```

### Setup Commands

```bash
# Create new repository
mkdir aws-pricing-calculator-mcp
cd aws-pricing-calculator-mcp

# Copy files from current project
cp -r mcp_server/ .
cp -r scripts/ .
cp pyproject.toml .
cp MCP_SERVER_README.md README.md
cp test_mcp_server.py .
cp test_mcp_stdio.py .

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.venv/
venv/
*.json.bak
*_estimate.json
*_url.txt
test_*.json
EOF

# Initialize git
git init
git add .
git commit -m "Initial commit: AWS Pricing Calculator MCP Server"

# Create GitHub repository and push
gh repo create aws-pricing-calculator-mcp --public --source=. --remote=origin
git push -u origin main
```

### Test Before Publishing

```bash
# Test locally
python3 test_mcp_server.py
python3 test_mcp_stdio.py

# Test with uvx (local)
uvx --from . aws-pricing-calculator-mcp
```

### Publish to PyPI (Optional but Recommended)

```bash
# Build the package
uv build

# Publish to PyPI
uv publish

# Or use twine
pip install twine
twine upload dist/*
```

## Step 2: Create Power Repository

### Files to Include

```
aws-pricing-calculator-power/
├── POWER.md
├── mcp.json
├── steering/
│   ├── api_endpoints.md
│   ├── service_formats.md
│   └── troubleshooting.md
└── README.md
```

### Setup Commands

```bash
# Create new repository
mkdir aws-pricing-calculator-power
cd aws-pricing-calculator-power

# Copy files from current project
cp POWER.md .
cp mcp.json .
cp -r steering/ .

# Create README for the power
cat > README.md << 'EOF'
# AWS Pricing Calculator Power

Kiro Power for generating shareable AWS Pricing Calculator URLs from architecture descriptions.

## Installation

### Prerequisites

1. Install [uv](https://docs.astral.sh/uv/):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install this power in Kiro:
   - Open Powers UI in Kiro
   - Add Custom Power → GitHub Repository
   - Enter: `YOUR_USERNAME/aws-pricing-calculator-power`

### What Gets Installed

- Power documentation and workflows
- MCP server configuration (automatically downloads MCP server via uvx)

## Usage

Trigger the power with phrases like:
- "Create an AWS cost estimate for this architecture"
- "Generate a pricing calculator URL for this blog post"
- "Cost this architecture on AWS"

## MCP Server

This power uses the [aws-pricing-calculator-mcp](https://github.com/YOUR_USERNAME/aws-pricing-calculator-mcp) server, which is automatically downloaded and run via `uvx`.

## License

MIT
EOF

# Initialize git
git init
git add .
git commit -m "Initial commit: AWS Pricing Calculator Power"

# Create GitHub repository and push
gh repo create aws-pricing-calculator-power --public --source=. --remote=origin
git push -u origin main
```

## Step 3: Update References

### In MCP Server Repository

Update `pyproject.toml`:
```toml
[project.urls]
Homepage = "https://github.com/YOUR_USERNAME/aws-pricing-calculator-mcp"
Repository = "https://github.com/YOUR_USERNAME/aws-pricing-calculator-mcp"
```

### In Power Repository

Update `POWER.md` and `README.md` with actual GitHub URLs.

## Step 4: Test End-to-End

### Test MCP Server

```bash
# Test that uvx can download and run the server
uvx aws-pricing-calculator-mcp

# Should start and wait for JSON-RPC input
# Press Ctrl+C to stop
```

### Test Power in Kiro

1. Install the power from GitHub
2. Verify MCP server connects
3. Test with: "List all AWS services available in the pricing calculator"

## Step 5: Distribution

### Option 1: GitHub Only

Users install via:
```
Kiro Powers UI → Add Custom Power → GitHub Repository
→ YOUR_USERNAME/aws-pricing-calculator-power
```

### Option 2: Submit to Kiro Recommended Powers

1. Ensure both repositories are public
2. Test thoroughly
3. Submit via: https://kiro.dev/powers/submit/

## Maintenance

### Updating the MCP Server

```bash
cd aws-pricing-calculator-mcp

# Make changes
# Update version in pyproject.toml
# Commit and push

git add .
git commit -m "Update: description of changes"
git push

# Publish new version to PyPI
uv build
uv publish
```

### Updating the Power

```bash
cd aws-pricing-calculator-power

# Make changes to POWER.md or steering files
# Commit and push

git add .
git commit -m "Update: description of changes"
git push
```

Users will automatically get updates when they update the power in Kiro.

## Troubleshooting

### "uvx: command not found"

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "Package not found: aws-pricing-calculator-mcp"

If not published to PyPI, users need to install from GitHub:
```json
{
  "mcpServers": {
    "aws-pricing-calculator": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/YOUR_USERNAME/aws-pricing-calculator-mcp", "aws-pricing-calculator-mcp"]
    }
  }
}
```

### MCP Server Won't Start

Check logs in Kiro MCP panel. Common issues:
- uv not installed
- Python version < 3.10
- Network issues downloading package

## Benefits of This Architecture

✅ **Clean separation**: Power and MCP server are independent  
✅ **Easy distribution**: Users only need uv installed  
✅ **Automatic updates**: uvx fetches latest version  
✅ **No local scripts**: Everything downloaded from GitHub/PyPI  
✅ **Standard approach**: Follows MCP server best practices  
✅ **Portable**: Works on any system with uv  

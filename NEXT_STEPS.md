# Next Steps: Publishing Your AWS Pricing Calculator Power

## ✅ What We've Built

You now have a complete MCP-based AWS Pricing Calculator power with:

1. **MCP Server** - Python server with 4 tools (discover_services, build_estimate, save_estimate, get_region_name)
2. **Power Documentation** - POWER.md with complete workflow and tool documentation
3. **Steering Files** - API endpoints, service formats, and troubleshooting guides
4. **Clean Distribution** - Uses `uvx` for automatic MCP server installation

## 📦 Current Project Structure

```
aws-pricing-calculator/
├── mcp_server/              # MCP server code (for separate repo)
│   ├── server.py
│   └── tools.py
├── scripts/                 # Python scripts (for separate repo)
│   ├── calc_utils.py
│   ├── calc_discover.py
│   ├── calc_build.py
│   └── calc_save.py
├── steering/                # Power steering files
│   ├── api_endpoints.md
│   ├── service_formats.md
│   └── troubleshooting.md
├── POWER.md                 # Power documentation
├── mcp.json                 # MCP configuration (uses uvx)
├── pyproject.toml           # Python package config
├── test_mcp_server.py       # Tests
├── test_mcp_stdio.py        # Tests
└── DEPLOYMENT_GUIDE.md      # Full deployment instructions
```

## 🚀 Ready to Deploy

### Option 1: Quick Test in Kiro (Local)

Test the power locally before publishing:

1. **Ensure uv is installed:**
   ```bash
   uv --version
   ```

2. **Update the power in Kiro:**
   - Powers UI → Your power → Check for Updates → Update

3. **Reconnect MCP server:**
   - MCP Servers view → aws-pricing-calculator → Reconnect

4. **Test:**
   ```
   activate aws-pricing-calculator
   ```
   
   Should now show 4 tools available!

### Option 2: Publish to GitHub (Recommended)

Follow the **DEPLOYMENT_GUIDE.md** to create two repositories:

1. **aws-pricing-calculator-mcp** (MCP server)
   - Contains: mcp_server/, scripts/, pyproject.toml
   - Users install via: `uvx aws-pricing-calculator-mcp`

2. **aws-pricing-calculator-power** (Kiro Power)
   - Contains: POWER.md, mcp.json, steering/
   - Users install via: Kiro Powers UI → GitHub

## 🧪 Testing Checklist

Before publishing, verify:

- [ ] `uvx --from . aws-pricing-calculator-mcp` starts the server
- [ ] `python3 test_mcp_server.py` passes all tests
- [ ] `python3 test_mcp_stdio.py` shows 4 tools
- [ ] Power installs in Kiro without errors
- [ ] MCP server connects (check Kiro MCP logs)
- [ ] Tools are visible when activating power
- [ ] Test workflow: "List all AWS services"

## 📝 Before Publishing

### Update These Files

1. **pyproject.toml** - Replace `YOUR_USERNAME` with your GitHub username
2. **MCP_SERVER_README.md** - Replace `YOUR_USERNAME` with your GitHub username
3. **POWER.md** - Update license and attribution sections
4. **README.md** (create for power repo) - Add installation instructions

### Create GitHub Repositories

```bash
# 1. Create MCP server repository
mkdir ../aws-pricing-calculator-mcp
cp -r mcp_server scripts pyproject.toml test_*.py ../aws-pricing-calculator-mcp/
cp MCP_SERVER_README.md ../aws-pricing-calculator-mcp/README.md
cd ../aws-pricing-calculator-mcp
git init
git add .
git commit -m "Initial commit"
gh repo create aws-pricing-calculator-mcp --public --source=. --remote=origin
git push -u origin main

# 2. Create power repository
cd ..
mkdir aws-pricing-calculator-power
cp aws-pricing-calculator/POWER.md aws-pricing-calculator-power/
cp aws-pricing-calculator/mcp.json aws-pricing-calculator-power/
cp -r aws-pricing-calculator/steering aws-pricing-calculator-power/
cd aws-pricing-calculator-power
# Create README.md (see DEPLOYMENT_GUIDE.md for template)
git init
git add .
git commit -m "Initial commit"
gh repo create aws-pricing-calculator-power --public --source=. --remote=origin
git push -u origin main
```

## 🎯 Installation for Users

Once published, users will:

1. **Install uv** (one-time):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install power in Kiro:**
   - Powers UI → Add Custom Power → GitHub Repository
   - Enter: `YOUR_USERNAME/aws-pricing-calculator-power`

3. **Use the power:**
   - "Create an AWS cost estimate for this architecture"
   - MCP server automatically downloads via uvx

## 🐛 Troubleshooting

### "No tools available" when activating

**Cause:** MCP server not connecting

**Fix:**
1. Check Kiro MCP logs for errors
2. Verify `uvx aws-pricing-calculator-mcp` works manually
3. Reconnect MCP server in Kiro

### "spawn python3 ENOENT"

**Cause:** Using `python3` command instead of `uvx`

**Fix:** Ensure mcp.json uses:
```json
{
  "command": "uvx",
  "args": ["aws-pricing-calculator-mcp"]
}
```

### "Package not found"

**Cause:** MCP server not published to PyPI or GitHub

**Fix:** Use GitHub URL in mcp.json:
```json
{
  "command": "uvx",
  "args": ["--from", "git+https://github.com/YOUR_USERNAME/aws-pricing-calculator-mcp", "aws-pricing-calculator-mcp"]
}
```

## 📚 Documentation

- **DEPLOYMENT_GUIDE.md** - Complete deployment instructions
- **MCP_SERVER_GUIDE.md** - Technical details about the MCP server
- **POWER.md** - User-facing power documentation

## 🎉 Success Criteria

Your power is ready when:

✅ MCP server starts via `uvx`  
✅ Power installs in Kiro without errors  
✅ 4 tools visible when activating power  
✅ Test workflow completes successfully  
✅ Documentation is clear and complete  

## 💡 Optional Enhancements

After initial release, consider:

- [ ] Publish MCP server to PyPI for faster installation
- [ ] Add more service formats to steering/service_formats.md
- [ ] Create video tutorial
- [ ] Submit to Kiro recommended powers
- [ ] Add CI/CD for automated testing
- [ ] Create example estimates repository

---

**You're ready to publish!** Follow the DEPLOYMENT_GUIDE.md for step-by-step instructions.

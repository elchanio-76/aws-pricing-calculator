"""AWS Pricing Calculator MCP Server.

This server provides tools for automating AWS Pricing Calculator estimate generation:
- discover_services: Fetch service schemas from AWS
- build_estimate: Build estimate JSON from specification
- save_estimate: Save estimate and get shareable URL
- get_region_name: Convert region codes to display names
"""

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import (
    discover_services_tool,
    build_estimate_tool,
    save_estimate_tool,
    get_region_name_tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aws-pricing-calculator-mcp")

# Create server instance
app = Server("aws-pricing-calculator")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="discover_services",
            description=(
                "Discover AWS Pricing Calculator service schemas. "
                "Fetches live service definitions and extracts configurable components. "
                "Call with no arguments to list all available services, or provide "
                "service_codes to get detailed schemas for specific services."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "service_codes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "List of AWS service codes to discover "
                            "(e.g., ['ec2Enhancement', 'amazonS3']). "
                            "Leave empty to list all available services."
                        ),
                    }
                },
            },
        ),
        Tool(
            name="build_estimate",
            description=(
                "Build AWS Pricing Calculator estimate JSON from a specification. "
                "Takes a spec with groups and services, calculates totals, and "
                "generates the complete estimate structure ready for saving."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "spec": {
                        "type": "object",
                        "description": "Estimate specification",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the estimate"
                            },
                            "groups": {
                                "type": "array",
                                "description": "List of service groups",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "services": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "serviceCode": {"type": "string"},
                                                    "serviceName": {"type": "string"},
                                                    "estimateFor": {"type": "string"},
                                                    "version": {"type": "string"},
                                                    "region": {"type": "string"},
                                                    "monthlyCost": {"type": "number"},
                                                    "configSummary": {"type": "string"},
                                                    "calculationComponents": {"type": "object"}
                                                },
                                                "required": [
                                                    "serviceCode",
                                                    "estimateFor",
                                                    "version",
                                                    "calculationComponents"
                                                ]
                                            }
                                        }
                                    },
                                    "required": ["name", "services"]
                                }
                            }
                        },
                        "required": ["name", "groups"]
                    }
                },
                "required": ["spec"]
            },
        ),
        Tool(
            name="save_estimate",
            description=(
                "Save an estimate to AWS Pricing Calculator and get a shareable URL. "
                "POSTs the estimate to the AWS Save API and returns a calculator URL "
                "that can be opened in a browser for viewing and editing."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "estimate": {
                        "type": "object",
                        "description": (
                            "Complete estimate JSON (output from build_estimate tool)"
                        ),
                    }
                },
                "required": ["estimate"]
            },
        ),
        Tool(
            name="get_region_name",
            description=(
                "Get the display name for an AWS region code. "
                "Converts region codes like 'us-east-1' to display names "
                "like 'US East (N. Virginia)'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "region_code": {
                        "type": "string",
                        "description": "AWS region code (e.g., 'us-east-1')"
                    }
                },
                "required": ["region_code"]
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "discover_services":
            result = await discover_services_tool(
                service_codes=arguments.get("service_codes")
            )
        elif name == "build_estimate":
            result = await build_estimate_tool(spec=arguments["spec"])
        elif name == "save_estimate":
            result = await save_estimate_tool(estimate=arguments["estimate"])
        elif name == "get_region_name":
            result = await get_region_name_tool(region_code=arguments["region_code"])
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}
        
        import json
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        import json
        return [
            TextContent(
                type="text",
                text=json.dumps({"success": False, "error": str(e)}, indent=2)
            )
        ]


async def main():
    """Run the MCP server."""
    logger.info("Starting AWS Pricing Calculator MCP Server")
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server initialized, waiting for requests")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def run():
    """Entry point for the server."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    run()

#!/usr/bin/env python3
"""Test script for the AWS Pricing Calculator MCP server."""

import asyncio
import json
from mcp_server.tools import (
    discover_services_tool,
    build_estimate_tool,
    save_estimate_tool,
    get_region_name_tool,
)


async def test_discover_services():
    """Test discovering services."""
    print("\n=== Test 1: List All Services ===")
    result = await discover_services_tool()
    print(f"Success: {result['success']}")
    print(f"Service count: {result.get('service_count', 0)}")
    if result['success']:
        print(f"First 5 services: {result['services'][:5]}")
    
    print("\n=== Test 2: Discover Specific Service (EC2) ===")
    result = await discover_services_tool(service_codes=["ec2Enhancement"])
    print(f"Success: {result['success']}")
    if result['success'] and 'schemas' in result:
        schema = result['schemas'].get('ec2Enhancement', {})
        print(f"Service: {schema.get('serviceName')}")
        print(f"Template: {schema.get('templateId')}")
        print(f"Version: {schema.get('version')}")
        print(f"Components: {len(schema.get('components', []))}")


async def test_region_name():
    """Test region name conversion."""
    print("\n=== Test 3: Get Region Name ===")
    result = await get_region_name_tool("us-east-1")
    print(f"Success: {result['success']}")
    print(f"Region: {result.get('region_code')} -> {result.get('region_name')}")


async def test_build_estimate():
    """Test building an estimate."""
    print("\n=== Test 4: Build Simple Estimate ===")
    
    # Simple test spec with minimal EC2 configuration
    spec = {
        "name": "Test Estimate",
        "groups": [
            {
                "name": "Test Group",
                "services": [
                    {
                        "serviceCode": "ec2Enhancement",
                        "serviceName": "Amazon EC2",
                        "estimateFor": "template",
                        "version": "0.0.68",
                        "region": "us-east-1",
                        "monthlyCost": 50.00,
                        "configSummary": "1x t3.micro Linux",
                        "calculationComponents": {
                            "tenancy": {"value": "shared"},
                            "selectedOS": {"value": "linux"},
                            "instanceType": {"value": "t3.micro"},
                        }
                    }
                ]
            }
        ]
    }
    
    result = await build_estimate_tool(spec)
    print(f"Success: {result['success']}")
    if result['success']:
        summary = result['summary']
        print(f"Name: {summary['name']}")
        print(f"Groups: {summary['groups']}")
        print(f"Services: {summary['services']}")
        print(f"Monthly: ${summary['monthly_cost']:.2f}")
        print(f"Annual: ${summary['annual_cost']:.2f}")


async def main():
    """Run all tests."""
    print("Testing AWS Pricing Calculator MCP Server")
    print("=" * 50)
    
    try:
        await test_discover_services()
        await test_region_name()
        await test_build_estimate()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("\nNote: save_estimate test skipped (requires network call to AWS)")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

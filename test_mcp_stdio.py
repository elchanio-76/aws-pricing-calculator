#!/usr/bin/env python3
"""Test MCP server via stdio (simulates how Kiro calls it)."""

import json
import subprocess
import sys

def test_mcp_server():
    """Test the MCP server by sending JSON-RPC requests."""
    
    # Start the MCP server
    proc = subprocess.Popen(
        [sys.executable, "-m", "mcp_server.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Send initialize request
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("Sending initialize request...")
        proc.stdin.write(json.dumps(initialize_request) + "\n")
        proc.stdin.flush()
        
        # Read response
        response_line = proc.stdout.readline()
        print(f"Response: {response_line}")
        
        if response_line:
            response = json.loads(response_line)
            print(f"✅ Server responded: {json.dumps(response, indent=2)}")
            
            # Send tools/list request
            list_tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            
            print("\nSending tools/list request...")
            proc.stdin.write(json.dumps(list_tools_request) + "\n")
            proc.stdin.flush()
            
            # Read tools response
            tools_response_line = proc.stdout.readline()
            print(f"Tools response: {tools_response_line}")
            
            if tools_response_line:
                tools_response = json.loads(tools_response_line)
                print(f"✅ Tools list: {json.dumps(tools_response, indent=2)}")
        else:
            print("❌ No response from server")
            stderr = proc.stderr.read()
            if stderr:
                print(f"Server stderr: {stderr}")
    
    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    test_mcp_server()

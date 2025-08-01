#!/usr/bin/env python3
"""
Simple test script for the DeepWiki MCP server.
This script tests the MCP server functionality without requiring a full MCP client.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.mcp_server import query_repository, get_repository_file_content, list_supported_languages

async def test_mcp_server():
    """Test the MCP server tools."""
    print("Testing DeepWiki MCP Server...")
    
    print("\n1. Testing list_supported_languages...")
    try:
        languages = await list_supported_languages()
        print(f"✓ Supported languages: {languages[:100]}...")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n2. Testing query_repository with a simple query...")
    try:
        result = await query_repository(
            repo_url="https://github.com/microsoft/vscode",
            query="What is this repository about?",
            provider="google"
        )
        print(f"✓ Query result: {result[:200]}...")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n3. Testing get_repository_file_content...")
    try:
        content = await get_repository_file_content(
            repo_url="https://github.com/microsoft/vscode",
            file_path="README.md"
        )
        print(f"✓ File content: {content[:100]}...")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\nMCP Server test completed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())

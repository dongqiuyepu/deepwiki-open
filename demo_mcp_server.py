#!/usr/bin/env python3
"""
Demo script showing how to use the DeepWiki MCP server.
This script demonstrates the MCP server functionality with mock data.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.mcp_server import list_supported_languages, get_repository_file_content

async def demo_mcp_server():
    """Demonstrate the MCP server functionality."""
    print("🔌 DeepWiki MCP Server Demo")
    print("=" * 50)
    
    print("\n1. 🌍 Supported Languages:")
    try:
        languages = await list_supported_languages()
        print(languages)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n2. 📄 File Content Retrieval:")
    try:
        content = await get_repository_file_content(
            repo_url="https://github.com/microsoft/vscode",
            file_path="README.md"
        )
        print(f"✅ Successfully retrieved README.md ({len(content)} characters)")
        print(f"Preview: {content[:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n3. 🤖 Repository Query (requires API keys):")
    print("To test repository queries, set the following environment variables:")
    print("  export OPENAI_API_KEY='your_openai_api_key'")
    print("  export GOOGLE_API_KEY='your_google_api_key'  # optional")
    print("\nThen run:")
    print("  python api/run_mcp_server.py")
    print("\nOr use with Claude for Desktop by adding to claude_desktop_config.json:")
    print("""  {
    "mcpServers": {
      "deepwiki": {
        "command": "python",
        "args": ["/absolute/path/to/deepwiki-open/api/run_mcp_server.py"],
        "env": {
          "OPENAI_API_KEY": "your_openai_api_key",
          "GOOGLE_API_KEY": "your_google_api_key"
        }
      }
    }
  }""")
    
    print("\n✅ MCP Server Demo Complete!")
    print("📖 See api/MCP_SERVER.md for detailed setup instructions.")

if __name__ == "__main__":
    asyncio.run(demo_mcp_server())

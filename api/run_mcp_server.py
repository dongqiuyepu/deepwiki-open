#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

load_dotenv()

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

required_env_vars = ['OPENAI_API_KEY']
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    print(f"Warning: Missing environment variables: {', '.join(missing_vars)}", file=sys.stderr)
    print("Some functionality may not work correctly without these variables.", file=sys.stderr)

google_api_key = os.environ.get('GOOGLE_API_KEY')
if google_api_key:
    import google.generativeai as genai
    genai.configure(api_key=google_api_key)

from api.mcp_server import mcp

if __name__ == "__main__":
    mcp.run(transport='stdio')

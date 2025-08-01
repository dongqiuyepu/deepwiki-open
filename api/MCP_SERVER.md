# DeepWiki MCP Server

This MCP (Model Context Protocol) server provides intelligent repository analysis capabilities using the DeepWiki RAG system.

## Features

The server exposes the following tools:

### query_repository
Query a repository using RAG to get intelligent answers about the codebase.

**Parameters:**
- `repo_url` (required): URL of the repository (e.g., https://github.com/owner/repo)
- `query` (required): The question to ask about the repository
- `repo_type`: Type of repository (github, gitlab, bitbucket) - default: "github"
- `access_token`: Personal access token for private repositories
- `provider`: Model provider (google, openai, openrouter, ollama, azure) - default: "google"
- `model`: Specific model name to use
- `language`: Language for the response (en, ja, zh, es, kr, vi, etc.) - default: "en"
- `excluded_dirs`: Comma-separated directories to exclude
- `excluded_files`: Comma-separated file patterns to exclude
- `included_dirs`: Comma-separated directories to include exclusively
- `included_files`: Comma-separated file patterns to include exclusively

### get_repository_file_content
Get the content of a specific file from a repository.

**Parameters:**
- `repo_url` (required): URL of the repository
- `file_path` (required): Path to the file within the repository
- `repo_type`: Type of repository (github, gitlab, bitbucket) - default: "github"
- `access_token`: Personal access token for private repositories

### list_supported_languages
List the supported languages for repository analysis and responses.

## Setup

1. Ensure you have the required environment variables set:
   ```bash
   OPENAI_API_KEY=your_openai_api_key  # Required for embeddings
   GOOGLE_API_KEY=your_google_api_key  # Optional, for Google models
   # Add other API keys as needed
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the MCP server:
   ```bash
   python api/run_mcp_server.py
   ```

## Usage with MCP Clients

### Claude for Desktop

Add to your `claude_desktop_config.json`:

```json
{
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
}
```

### Example Queries

- "What is the main purpose of this repository?"
- "How does the authentication system work?"
- "Explain the database schema"
- "What are the main API endpoints?"
- "How do I set up the development environment?"

## Troubleshooting

- Ensure all required environment variables are set
- Check that the repository URL is accessible
- For private repositories, provide a valid access token
- Large repositories may take time to process initially

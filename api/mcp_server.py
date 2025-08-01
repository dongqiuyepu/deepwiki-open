import logging
import os
from typing import Any, Optional, List
from urllib.parse import unquote
from mcp.server.fastmcp import FastMCP
from api.rag import RAG
from api.config import configs
from api.data_pipeline import count_tokens, get_file_content
from api.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP("deepwiki")

_rag_cache = {}

async def get_or_create_rag(repo_url: str, repo_type: str = "github", 
                          access_token: Optional[str] = None,
                          provider: str = "google", model: Optional[str] = None,
                          excluded_dirs: Optional[List[str]] = None,
                          excluded_files: Optional[List[str]] = None,
                          included_dirs: Optional[List[str]] = None,
                          included_files: Optional[List[str]] = None) -> RAG:
    cache_key = f"{repo_url}:{repo_type}:{provider}:{model}"
    
    if cache_key not in _rag_cache:
        try:
            logger.info(f"Creating new RAG instance for {repo_url}")
            rag_instance = RAG(provider=provider, model=model)
            rag_instance.prepare_retriever(
                repo_url, repo_type, access_token or "",
                excluded_dirs or [], excluded_files or [], 
                included_dirs or [], included_files or []
            )
            _rag_cache[cache_key] = rag_instance
            logger.info(f"RAG instance created and cached for {repo_url}")
        except Exception as e:
            logger.error(f"Error creating RAG instance: {str(e)}")
            raise
    
    return _rag_cache[cache_key]

@mcp.tool()
async def query_repository(
    repo_url: str,
    query: str,
    repo_type: str = "github",
    access_token: Optional[str] = None,
    provider: str = "google",
    model: Optional[str] = None,
    language: str = "en",
    excluded_dirs: Optional[str] = None,
    excluded_files: Optional[str] = None,
    included_dirs: Optional[str] = None,
    included_files: Optional[str] = None
) -> str:
    """Query a repository using RAG to get intelligent answers about the codebase.
    
    Args:
        repo_url: URL of the repository to query (e.g., https://github.com/owner/repo)
        query: The question to ask about the repository
        repo_type: Type of repository (github, gitlab, bitbucket)
        access_token: Personal access token for private repositories
        provider: Model provider (google, openai, openrouter, ollama, azure)
        model: Specific model name to use
        language: Language for the response (en, ja, zh, es, kr, vi, etc.)
        excluded_dirs: Comma-separated directories to exclude
        excluded_files: Comma-separated file patterns to exclude
        included_dirs: Comma-separated directories to include exclusively
        included_files: Comma-separated file patterns to include exclusively
    """
    try:
        excluded_dirs_list = None
        excluded_files_list = None
        included_dirs_list = None
        included_files_list = None
        
        if excluded_dirs:
            excluded_dirs_list = [unquote(d.strip()) for d in excluded_dirs.split(',') if d.strip()]
        if excluded_files:
            excluded_files_list = [unquote(f.strip()) for f in excluded_files.split(',') if f.strip()]
        if included_dirs:
            included_dirs_list = [unquote(d.strip()) for d in included_dirs.split(',') if d.strip()]
        if included_files:
            included_files_list = [unquote(f.strip()) for f in included_files.split(',') if f.strip()]

        rag_instance = await get_or_create_rag(
            repo_url, repo_type, access_token, provider, model,
            excluded_dirs_list, excluded_files_list, 
            included_dirs_list, included_files_list
        )
        
        tokens = count_tokens(query, provider == "ollama")
        if tokens > 8000:
            logger.warning(f"Query exceeds recommended token limit ({tokens} > 8000)")
            return "Query is too long. Please try a shorter, more specific question."
        
        logger.info(f"Processing query for {repo_url}: {query[:100]}...")
        result = rag_instance(query, language=language)
        
        if result and len(result) > 0 and hasattr(result[0], 'answer'):
            answer = result[0].answer
            logger.info(f"Successfully generated answer for {repo_url}")
            return answer
        else:
            logger.warning(f"No answer generated for query: {query}")
            return "I couldn't generate an answer for your question. Please try rephrasing or asking about a different aspect of the repository."
            
    except ValueError as e:
        if "No valid documents with embeddings found" in str(e):
            logger.error(f"No valid embeddings found for {repo_url}: {str(e)}")
            return "Unable to analyze this repository. This may be due to embedding issues or the repository being empty/inaccessible."
        else:
            logger.error(f"ValueError in query_repository: {str(e)}")
            return f"Error processing repository: {str(e)}"
    except Exception as e:
        logger.error(f"Error in query_repository: {str(e)}")
        return f"An error occurred while processing your query: {str(e)}"

@mcp.tool()
async def get_repository_file_content(
    repo_url: str,
    file_path: str,
    repo_type: str = "github",
    access_token: Optional[str] = None
) -> str:
    """Get the content of a specific file from a repository.
    
    Args:
        repo_url: URL of the repository
        file_path: Path to the file within the repository
        repo_type: Type of repository (github, gitlab, bitbucket)
        access_token: Personal access token for private repositories
    """
    try:
        logger.info(f"Fetching file content: {file_path} from {repo_url}")
        content = get_file_content(repo_url, file_path, repo_type, access_token or "")
        return content
    except Exception as e:
        logger.error(f"Error fetching file content: {str(e)}")
        return f"Error fetching file content: {str(e)}"

@mcp.tool()
async def list_supported_languages() -> str:
    """List the supported languages for repository analysis and responses."""
    try:
        supported_langs = configs["lang_config"]["supported_languages"]
        default_lang = configs["lang_config"]["default"]
        
        lang_list = []
        for code, name in supported_langs.items():
            marker = " (default)" if code == default_lang else ""
            lang_list.append(f"- {code}: {name}{marker}")
        
        return "Supported languages:\n" + "\n".join(lang_list)
    except Exception as e:
        logger.error(f"Error listing languages: {str(e)}")
        return "Error retrieving supported languages."

if __name__ == "__main__":
    mcp.run(transport='stdio')

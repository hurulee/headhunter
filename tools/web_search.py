import os

from langchain_core.tools import tool
from tavily import TavilyClient


def create_web_search_tool():
    """Create and return the web search tool using Tavily."""
    client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

    @tool
    def search_web(query: str) -> str:
        """Search the web for career information, job market data, salary ranges, industry trends,
        and specific roles."""
        results = client.search(query, max_results=5)
        if not results.get("results"):
            return "No results found."
        chunks = []
        for result in results["results"]:
            title = result.get("title", "")
            url = result.get("url", "")
            content = result.get("content", "")
            chunks.append(f"**{title}**\n{url}\n{content}")
        return "\n\n---\n\n".join(chunks)

    return search_web

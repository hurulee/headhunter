from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from prompts.research import RESEARCH_PROMPT
from tools.knowledge import load_knowledge_base
from tools.web_search import create_web_search_tool


def create_research_agent(llm: ChatOpenAI, base_url: str, knowledge_dir: str):
    """Create and return the Research Agent."""
    search_knowledge = load_knowledge_base(base_url, knowledge_dir)
    search_web = create_web_search_tool()
    tools = [search_knowledge, search_web]

    memory = MemorySaver()
    agent = create_agent(llm, tools, system_prompt=RESEARCH_PROMPT, checkpointer=memory)
    return agent

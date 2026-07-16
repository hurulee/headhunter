from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from prompts.discovery import DISCOVERY_PROMPT
from tools.knowledge import load_knowledge_base


def create_discovery_agent(llm: ChatOpenAI, base_url: str, knowledge_dir: str):
    """Create and return the Discovery Agent."""
    search_knowledge = load_knowledge_base(base_url, knowledge_dir)
    tools = [search_knowledge]

    memory = MemorySaver()
    agent = create_agent(llm, tools, system_prompt=DISCOVERY_PROMPT, checkpointer=memory)
    return agent

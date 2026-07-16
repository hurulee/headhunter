from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import MemorySaver

from config import SUMMARY_TRIGGER_TOKENS, SUMMARY_KEEP_MESSAGES
from prompts.research import RESEARCH_PROMPT
from tools.knowledge import load_knowledge_base
from tools.web_search import create_web_search_tool


def create_research_agent(llm: ChatOpenAI, base_url: str, knowledge_dir: str):
    """Create and return the Research Agent."""
    search_knowledge = load_knowledge_base(base_url, knowledge_dir)
    search_web = create_web_search_tool()
    tools = [search_knowledge, search_web]

    summarizer = SummarizationMiddleware(
        model=llm,
        trigger=("tokens", SUMMARY_TRIGGER_TOKENS),
        keep=("messages", SUMMARY_KEEP_MESSAGES),
    )

    memory = MemorySaver()
    agent = create_agent(
        llm,
        tools,
        system_prompt=RESEARCH_PROMPT,
        checkpointer=memory,
        middleware=[summarizer],
    )
    return agent

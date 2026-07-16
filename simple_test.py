from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

# Connect to local LM Studio
llm = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    model="gemma-4-E4B-it"
)

# Define a simple tool the agent can use
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

# Create the agent with tools
agent = create_agent(llm, [multiply, add])

# Run it
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is 6 times 7, plus 10?"}]}
)

# Print the conversation
for msg in result["messages"]:
    print(f"\n{msg.type}: {msg.content}")
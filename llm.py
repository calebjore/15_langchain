from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool, ToolRuntime
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from pydantic import BaseModel
from langgraph.checkpoint.memory import InMemorySaver
import random

load_dotenv()

class Response(BaseModel):
    response: str

@tool
def rock_paper_scissors(runtime: ToolRuntime) -> str:
    """Use this when the user requests to play rock paper scissors
    or if they play a new move after a previous match. Don't tell 
    the user your move until the user has played theirs."""
    num = random.randint(0, 1001)
    play = ""
    if (num % 3) == 0:
        play = "rock"
    elif (num % 3) == 1:
        play = "paper"
    else:
        play = "scissors"

    return play

search_tool = DuckDuckGoSearchRun()

tools=[rock_paper_scissors, search_tool]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

agent = create_agent(
    model=llm,
    tools=tools,
    response_format=ToolStrategy(Response),
    checkpointer=InMemorySaver()
)

query = ""
print("Begin chatting! Type 'exit' to quit.")

while query.lower() != "exit":
    query = input("> ")

    if query.lower() == "exit":
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        {"configurable": {"thread_id": "1"}}
    )
    print("\n" + response['structured_response'].response + "\n")
    
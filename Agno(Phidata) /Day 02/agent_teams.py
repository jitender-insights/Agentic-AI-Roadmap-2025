from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.models.groq import Groq 
from dotenv import load_dotenv
load_dotenv()
import os 

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

## Web Agent 
web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    tools=[DuckDuckGoTools()],
    instructions="Always include sources",
    show_tool_calls=True,
    markdown=True,
)

## Finance Agent

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions="Use tables to display data",
    show_tool_calls=True,
    markdown=True,
)

## Teams of Agent
agent_team = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("What's the market outlook and financial performance of ITC ?", stream=True)

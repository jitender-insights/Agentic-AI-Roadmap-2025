from agno.agent import Agent 
from agno.models.groq import Groq 
from agno.models.ollama import Ollama 
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
load_dotenv()
import os 

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")


### Define the Agent
def create_agent():
    return(
        Agent(
    #model = Ollama(id = "deepseek-r1:1.5b"),
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    description="You are an enthusiastic news reporter with a flair for storytelling!",
    tools= [DuckDuckGoTools()],
    show_tool_calls=False,
    parse_response=True,
    structured_outputs=True,
    markdown=True
)
    )



## Print the response in the console

# agent.print_response("Tell me about a breaking news story from New York.", stream=True)


def get_news_repsonse(agent,query):
    try:
        resposne = agent.run(query)
        return resposne.content 
    except Exception as e:
        return f"Error getting response: :{str(e)}"

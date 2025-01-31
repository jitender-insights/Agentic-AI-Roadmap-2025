from agno.agent import Agent 
from agno.models.groq import Groq 
from agno.models.ollama import Ollama 
from dotenv import load_dotenv
load_dotenv()
import os 

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")


### Define the Agent

agent = Agent(
    #model = Groq(id = "deepseek-r1-distill-llama-70b"),
    model = Ollama(id = "deepseek-r1:1.5b"),
    description="You are an enthusiastic news reporter with a flair for storytelling!",
    markdown=True
)


## Print the response in the console

agent.print_response("Tell me about a breaking news story from New York.", stream=True)

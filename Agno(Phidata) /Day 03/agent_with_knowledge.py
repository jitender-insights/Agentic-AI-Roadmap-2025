from agno.agent import Agent 
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.google import Gemini
from agno.models.groq import Groq 
from agno.embedder.google import GeminiEmbedder
from agno.vectordb.lancedb import LanceDb
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db= LanceDb(
        table_name="recipes",
        uri="tmp/lancedb",
        embedder=GeminiEmbedder()
    )
)
knowledge_base.load(recreate=True)  #Comment out after first run


agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    knowledge=knowledge_base,
    show_tool_calls=True
)
agent.print_response("How to make Thai curry?", markdown=True)

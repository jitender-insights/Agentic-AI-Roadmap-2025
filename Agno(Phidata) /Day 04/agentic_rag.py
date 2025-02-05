"""Project Aim:
This project creates an AI-powered Thai cuisine chatbot that helps users learn about Thai recipes and culinary history. The key features are:

Interactive chat interface where users can ask questions
Access to a knowledge base of Thai recipes
Ability to search the web for additional information
Real-time responses in a user-friendly format"""

import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.embedder.google import GeminiEmbedder
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from dotenv import load_dotenv
import os

# Page configuration
st.set_page_config(
    page_title="Thai Cuisine Expert",
    page_icon="🍜",
    layout="centered"
)

# Add custom CSS
st.markdown("""
    <style>
    .stChat {
        padding: 20px;
    }
    .user-message {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .bot-message {
        background-color: #e8f0fe;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

def get_agent_response(agent, query):
    """Get response from the agent"""
    try:
        response = agent.run(query)
        return response.content
    except Exception as e:
        return f"Error getting response: {str(e)}"

def initialize_agent():
    """Initialize the Thai cuisine expert agent"""
    load_dotenv()
    
    # Set environment variables
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
    os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
    
    try:
        agent = Agent(
            model=Groq(id="deepseek-r1-distill-llama-70b"),
            description="You are a Thai cuisine expert!",
            instructions=[
                "Search your knowledge base for Thai recipes.",
                "If the question is better suited for the web, search the web to fill in gaps.",
                "Prefer the information in your knowledge base over the web results."
            ],
            knowledge=PDFUrlKnowledgeBase(
                urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
                vector_db=LanceDb(
                    uri="tmp/lancedb",
                    table_name="recipes",
                    search_type=SearchType.hybrid,
                    embedder=GeminiEmbedder(),
                ),
            ),
            tools=[DuckDuckGoTools()],
            show_tool_calls=False,
            markdown=True
        )
        
        # Load knowledge base if not already loaded
        if agent.knowledge is not None and not hasattr(agent.knowledge, '_loaded'):  
            ##_loaded is a custom flag we use to track if the knowledge base is loaded
            ## The underscore prefix _ indicates it's an internal tracking variable
            agent.knowledge.load()
            agent.knowledge._loaded = True
        
        return agent
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        return None

# Main app
def main():
    st.title("🍜 Thai Cuisine Expert")
    st.markdown("Ask me anything about Thai recipes and cuisine!")
    
    # Initialize agent
    if 'agent' not in st.session_state:
        with st.spinner("Initializing Thai cuisine expert..."):
            st.session_state.agent = initialize_agent()
    
    # Check if agent initialization was successful
    if st.session_state.agent is None:
        st.error("Failed to initialize the Thai cuisine expert. Please check your API keys and try again.")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.markdown(content)
    
    # Chat input
    if prompt := st.chat_input("Ask about Thai cuisine..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Our Thai cuisine expert is cooking up an answer..."):
                try:
                    response = get_agent_response(st.session_state.agent, prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main()
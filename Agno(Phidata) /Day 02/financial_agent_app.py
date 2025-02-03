import streamlit as st
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.models.groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Financial Market Analysis Agent",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("Financial Market Analysis Agent")
st.markdown("""
This application uses AI agents to analyze financial markets and companies by combining web search 
and financial data. Enter your query below to get comprehensive insights.
""")

def get_agent_response(agent, query):
    try:
        response = agent.run(query)
        return response.content
    except Exception as e:
        return f"Error getting response: {str(e)}"

# Initialize agents if they haven't been created
@st.cache_resource
def initialize_agents():
    # Set API key
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
    
    # Create Web Agent
    web_agent = Agent(
        name="Web Agent",
        role="Search the web for information",
        model=Groq(id="deepseek-r1-distill-llama-70b"),
        tools=[DuckDuckGoTools()],
        instructions="Always include sources",
        show_tool_calls=True,
        markdown=True,
    )

    # Create Finance Agent
    finance_agent = Agent(
        name="Finance Agent",
        role="Get financial data",
        model=Groq(id="deepseek-r1-distill-llama-70b"),
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
        instructions="Use tables to display data",
        show_tool_calls=True,
        markdown=True,
    )

    # Create Agent Team
    agent_team = Agent(
        team=[web_agent, finance_agent],
        model=Groq(id="deepseek-r1-distill-llama-70b"),
        instructions=["Always include sources", "Use tables to display data"],
        show_tool_calls=True,
        markdown=True,
    )
    
    return agent_team

# Initialize the agents
try:
    if 'agent_team' not in st.session_state:
        st.session_state.agent_team = initialize_agents()
    st.success("✅ Agents initialized successfully!")
except Exception as e:
    st.error(f"❌ Error initializing agents: {str(e)}")
    st.stop()

# Create a text input for the query
query = st.text_input(
    "Enter your query:",
    placeholder="Example: What's the market outlook and financial performance of AAPL?",
    key="query_input"
)

# Add a submit button
if st.button("🔍 Analyze", type="primary"):
    with st.spinner("🤖 Agents are analyzing your query..."):
        try:
            # Create expander for response
            with st.expander("📊 Analysis Results", expanded=True):
                # Get and display the response
                response = get_agent_response(st.session_state.agent_team, query)
                st.markdown(response)
                
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Made with ❤️ using Agno Agentic AI Framework and Streamlit</p>
</div>
""", unsafe_allow_html=True)
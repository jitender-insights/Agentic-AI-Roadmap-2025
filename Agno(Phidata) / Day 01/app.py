import streamlit as st 
from agent_with_tools import *


######## Confguire the page ########

st.set_page_config(
    page_title="News AI Reporter",
    page_icon="📰",
    layout="wide"
)

########### Header ##################

st.title("🎙️ AI News Reporter")
st.markdown("Get the latest news with an enthusiastic storytelling twist!")


######### Initialize session state   ###########


if 'agent' not in st.session_state:
    st.session_state.agent = create_agent()
    

######## Create Input area ###########

query = st.text_area(
    "What news would you like to hear about?",
    value = "Tell me about a breaking news story of ICC Champion Trophy 2025.",
    height = 100
)

######### Add search Button ###########

if st.button("🔍 Get News", type="primary"):
    with st.spinner("Our AI reporter is gathering the latest information..."):
        
        try:
            
            ## Get and display the response
            
            response = get_news_repsonse(st.session_state.agent, query)
            st.markdown(response)
            
        except Exception as e:
                st.error(f"An error occurred: {str(e)}")


###### Add sidebar with information ##########
with st.sidebar:
        st.header("About")
        st.markdown("""
        This AI News Reporter uses:
        - Groq's deepseek-r1-distill-llama-70b model
        - DuckDuckGo search integration
        - Real-time news gathering capabilities
        
        Enter any news-related query, and the AI reporter will gather and present 
        the information in an engaging way!
        """)

        st.header("Tips")
        st.markdown("""
        - Be specific in your queries
        - Try asking about recent events
        - Include relevant details like dates or locations
        - Ask for specific aspects of a news story
        """)




            
        




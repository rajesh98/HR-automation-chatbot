from fastapi import FastAPI
import os
#from models import models
#from database import engine


from fastapi.middleware.cors import CORSMiddleware
#from .config import settings

from langchain_community.utilities.sql_database import SQLDatabase
###from langchain.chains import create_sql_query_chain
###from langchain_openai import ChatOpenAI
###from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
###from langchain.memory import ChatMessageHistory
###from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate

##from operator import itemgetter

##from langchain_core.output_parsers import StrOutputParser
###from langchain_core.runnables import RunnablePassthrough
###from langchain_openai import ChatOpenAI

#from table_details import table_chain as select_table
#from .prompts import  answer_prompt
from langchain_utils import invoke_chain
#######from langchain_utils import  get_chain_param,  get_chain, get_chain_param

from dotenv import load_dotenv
import streamlit as st
###from typing import Dict, Any
from pydantic import BaseModel

###from openai import OpenAI
#**************************************************************
import uuid
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Theta-X Assistant", layout="wide")


#******************************************************************


#from .router import user,auth, question,quiz,slot,event,result,category,quiztype,room,participant, stateManagement, currentStatus, resend_mail, websocket_api, sdp, clear_db
#from router import leaves

#models.Base.metadata.create_all(bind=engine)



#summary = """Quizzit.in: Engaging Live Quizzes

#Join interactive live quizzes on Quizzit.in for real-time audio-video engagement. Compete, connect, and learn with participants worldwide. Explore diverse topics, flexible scheduling, and win prizes. Elevate your quizzing experience today at www.quizzit.in!"""

# app = FastAPI(
#     title="HR-Automate-Chatbot",
#     #description=description,
#     #summary=summary,
#     version="0.0.1",
# ) 

# """ db = get_db()
# print(db.get_usable_table_names())

# load_dotenv()

#######################OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
# LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY") """






# app.add_middleware( 
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT","DELETE"],
#     allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization','Access-Control-Allow-Origin'],
# )

# app.include_router(leaves.router)

# @app.get('/')
# def root():
#     return {"message": "Welcome To Quizzit"}



# """ app.add_middleware( 
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT","DELETE"],
#     allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization','Access-Control-Allow-Origin'],
# )

# app.include_router(user.router)
# app.include_router(quiztype.router)
# app.include_router(category.router)
# app.include_router(result.router)
# app.include_router(event.router)
# app.include_router(slot.router)
# app.include_router(quiz.router)
# app.include_router(question.router)
# app.include_router(auth.router)
# app.include_router(room.router)
# app.include_router(participant.router)
# app.include_router(stateManagement.router)
# app.include_router(currentStatus.router)
# app.include_router(resend_mail.router)
# app.include_router(websocket_api.router)
# app.include_router(sdp.router)
# app.include_router(clear_db.router)

# leave_quota_prompt  = """
# Here are the maximum leave quotas permitted for all employees. Use this info to find remaining leaves or leave balance:

# *   **Total Annual Leaves (All Types):** You can take a maximum of **30 paid days** of leave in total per year.

# This total is divided into the following specific categories:

# *   **Annual Leave:** Maximum **15 days** per year.
# *   **Sick Leave:** Maximum **10 days** per year.
# *   **Casual Leave:** Maximum **5 days** per year.
# *   **Unpaid Leave:** There is no strict internal limit on Unpaid Leave (subject to manager approval).
# """

# answer_prompt = PromptTemplate.from_template(
#     """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

# Question: {question}
# SQL Query: {query}
# SQL Result: {result}
# Answer: """
# )
class QueryInput(BaseModel):
    question: str

# @app.get('/')
# def root():
#     return {"message": "Welcome To Theta-X Agent"}

# @app.post("/chat", )
# def chat(query_input: QueryInput):
#     llm_response = invoke_chain(query_input.question, "")
#     return llm_response


def login_function(username: str, password: str) -> bool:
    """
    Placeholder for your actual login function.
    In a real app, this would check credentials against a database.
    """
    # Simulate a successful login for specific credentials
    if username == "gourab" and password == "test":
        st.session_state.employee_id = 3  # Store a dummy ID for the session
        st.session_state.full_name = "Gourab Saha"
        return True
    if username == "sandeep" and password == "test":
        st.session_state.employee_id = 1  # Store a dummy ID for the session
        st.session_state.full_name = "Sandeep Bera"
        return True
    if username == "rajesh" and password == "test":
        st.session_state.employee_id = 2  # Store a dummy ID for the session
        st.session_state.full_name = "Rajesh Kar"
        return True
    if username == "uday" and password == "test":
        st.session_state.employee_id = 12  # Store a dummy ID for the session
        st.session_state.full_name = "Uday Sadhukhan"
        return True
    return False


# #response = invoke_chain("my user id is 2. find  how many Sick leaves   I  can take. Do not use unnecessary Limit in sql clause. {leave_quota_prompt}", messages="none")

# #print(response)


# # --- SESSION STATE INITIALIZATION ---
def initialize_session_state():
    """Initializes necessary variables in Streamlit's session state."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'employee_id' not in st.session_state:
        st.session_state.employee_id = None
    if 'full_name' not in st.session_state:
        st.session_state.full_name = None

# # --- UI COMPONENTS ---

def login_screen():
    """Renders the login interface."""
    st.title("🤖 Theta-X Chatbot Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if login_function(username, password):
                st.session_state.logged_in = True
                # Rerun the app to switch to the chat interface
                st.rerun() 
            else:
                st.error("Invalid Username or Password.")

def chat_interface_old():
    """Renders the main chat interface."""
    st.title(f"👋 Welcome to Theta-X Agentic Assistant.")
    
    # 1. Display Chat History
    for role, message in st.session_state.chat_history:
        # Use Streamlit's chat elements for a modern look
        with st.chat_message(role):
            st.markdown(message)

    # 2. Handle User Input
    if prompt := st.chat_input("Ask me about your leave, or to apply for leave..."):
        # Add user's message to history
        st.session_state.chat_history.append(("user", prompt))
        
        # Rerender chat history immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call the chat function to get LLM response
        with st.spinner("Thinking..."):
            # Pass the employee_id for personalized data retrieval
            #print()
            #my_id = f"My Employee id is {st.session_state.employee_id} and my full name is {st.session_state.full_name}."
            #print(my_id)
            #new_prompt = f"{my_id} Now {prompt}"
            new_prompt = prompt
            llm_response = invoke_chain(new_prompt, st.session_state.chat_history)
            #####print(f"-----------LLM RES---------------------{llm_response}")
        
        # Add assistant's response to history
        st.session_state.chat_history.append(("assistant", llm_response))
        
        # Display assistant's response
        with st.chat_message("assistant"):
            st.markdown(llm_response)
        
        # Rerun to clear the chat input field
        st.rerun()

    # Logout button
    # if st.button("Logout", key="logout_btn"):
    #     st.session_state.logged_in = False
    #     st.session_state.chat_history = []
    #     st.session_state.employee_id = None
    #     st.session_state.full_name = None
    #     st.rerun()


#





#*************************************************************************************************

def apply_custom_styles():
    """Injects custom CSS for a modern, 'Agentic' look."""
    st.markdown("""
        <style>
        /* Main Chat Bubble Styling */
        [data-testid="stChatMessage"] {
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        /* Sidebar Chat History Buttons */
        .stButton > button {
            width: 100%;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
            background-color: transparent;
            text-align: left;
            padding: 10px;
            margin-bottom: 5px;
            transition: all 0.3s;
        }
        .stButton > button:hover {
            background-color: #f0f2f6;
            border-color: #ff4b4b;
        }
                
        .center-title-sidebar {
            text-align: center;
            
        }

        /* Title Styling */
        .main-title {
            background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0px;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_custom_css():
    st.markdown("""
        <style>
        /* Modern Title Styling */
        .main-title {
            background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0px;
        }
        
        /* Sidebar chat items */
        .stButton>button {
            border: none;
            background-color: transparent;
            text-align: left;
            font-size: 14px;
            color: #d1d1d1;
            padding: 10px 15px;
            width: 100%;
            border-radius: 8px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #2b2c32;
            color: white;
        }

        /* Message Bubble Tweaks */
        [data-testid="stChatMessage"] {
            background-color: #1e1f24;
            border: 1px solid #2d2e35;
            border-radius: 15px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
                
        .center-title-sidebar {
            text-align: center;
                color: #3a7bd5;
        }
        
        /* Suggestion Pills */
        .suggestion-btn {
            border: 1px solid #3a7bd5;
            border-radius: 20px;
            padding: 5px 15px;
            margin-right: 10px;
            font-size: 12px;
            color: #3a7bd5;
            display: inline-block;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)


# --- 2. SESSION STATE MANAGEMENT ---
def initialize_state():
    if "all_chats" not in st.session_state:
        # Dictionary to store {chat_id: {"title": str, "history": list}}
        st.session_state.all_chats = {}
    if "current_chat_id" not in st.session_state:
        # Start with a fresh chat ID
        new_id = str(uuid.uuid4())
        st.session_state.current_chat_id = new_id
        st.session_state.all_chats[new_id] = {"title": "New Chat", "history": []}

def get_current_history():
    return st.session_state.all_chats[st.session_state.current_chat_id]["history"]

# --- 3. SIDEBAR HISTORY COMPONENT ---
def render_sidebar():
    with st.sidebar:
        ##st.image("https://img.icons8.com/?size=100&id=48243&format=png&color=000000", use_container_width=False)
        #st.title("Chat History")
        st.markdown('<h1 class ="center-title-sidebar">Chat History</h1>', unsafe_allow_html=True)


        
        # New Chat Button
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            new_id = str(uuid.uuid4())
            st.session_state.all_chats[new_id] = {"title": "New Chat", "history": []}
            st.session_state.current_chat_id = new_id
            st.rerun()

        st.divider()

        # List Previous Chats
        for chat_id, chat_data in reversed(list(st.session_state.all_chats.items())):
            # Dynamic Title: Use the first user message as the button label
            title = chat_data["title"]
            if st.button(f"💬 {title[:25]}...", key=chat_id):
                st.session_state.current_chat_id = chat_id
                st.rerun()

# --- 4. MAIN INTERFACE ---
def chat_interface():
    apply_custom_styles()
    #apply_custom_css()
    render_sidebar()

    # Current context
    chat_id = st.session_state.current_chat_id
    history = st.session_state.all_chats[chat_id]["history"]

    st.markdown('<h1 class="main-title"> Welcome to Theta-X Agentic Assistant</h1>', unsafe_allow_html=True)
    st.caption("Find device status, Excellent/Moderate/Inactive devices, reason for Issues and lot more")

    # 1. Display Chat History
    for role, message in history:
        # Add custom avatars for a professional look
        avatar = "🤖" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message)

    # 2. Handle User Input
    if prompt := st.chat_input("Ask Here on device status, Excellent/Moderate/Inactive devices, reason for Issues and lot more...."):
        # Update Title if it's the first message
        if not history:
            st.session_state.all_chats[chat_id]["title"] = prompt

        # Append to history
        history.append(("user", prompt))
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Theta-X is thinking..."):
                # Placeholder for your invoke_chain function
                # llm_response = invoke_chain(prompt, history)
                llm_response = invoke_chain(prompt, history)
                
                st.markdown(llm_response)
                history.append(("assistant", llm_response))
        
        st.rerun()

# Run the app

#**************************************************************************************************

def format_device_data(text):
    """
    Optional: If the LLM returns a list, this helper can turn it 
    into a clean Streamlit Dataframe or Table for better UI.
    """
    if "Device ID" in text:
        # This is a placeholder logic: in a real app, you'd parse the LLM 
        # response or return a list of dicts from your tool/function.
        return st.info("💡 Pro Tip: You can view these devices in a table below.")
    return None


def main():
    initialize_session_state()
    
    if st.session_state.logged_in:
        chat_interface()
        
    else:
        initialize_state()
        chat_interface()
    
    


if __name__ == "__main__":
    
    main()

# """ """ @app.get('/')
# def root(): """
#    return {"message": "Welcome To HR automation"} """


# """ get_chain()


# st.title("Langchain NL2SQL Chatbot")

# # Set OpenAI API key from Streamlit secrets
# client = OpenAI(api_key=OPENAI_API_KEY)

# # Set a default model
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# # Initialize chat history
# if "messages" not in st.session_state:
#     # print("Creating session state")
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Display assistant response in chat message container
#     with st.spinner("Generating response..."):
#         with st.chat_message("assistant"):
#             response = invoke_chain(prompt,st.session_state.messages)
#             st.markdown(response)
#     st.session_state.messages.append({"role": "assistant", "content": response}) """











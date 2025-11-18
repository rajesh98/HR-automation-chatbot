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









#from .router import user,auth, question,quiz,slot,event,result,category,quiztype,room,participant, stateManagement, currentStatus, resend_mail, websocket_api, sdp, clear_db
#from router import leaves

#models.Base.metadata.create_all(bind=engine)



#summary = """Quizzit.in: Engaging Live Quizzes

#Join interactive live quizzes on Quizzit.in for real-time audio-video engagement. Compete, connect, and learn with participants worldwide. Explore diverse topics, flexible scheduling, and win prizes. Elevate your quizzing experience today at www.quizzit.in!"""

app = FastAPI(
    title="HR-Automate-Chatbot",
    #description=description,
    #summary=summary,
    version="0.0.1",
) 

# """ db = get_db()
# print(db.get_usable_table_names())

# load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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

@app.get('/')
def root():
    return {"message": "Welcome To HR Chatbot"}

@app.post("/chat", )
def chat(query_input: QueryInput):
    llm_response = invoke_chain(query_input.question, "")
    return llm_response


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
    st.title("🤖 HR Chatbot Login")
    
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

def chat_interface():
    """Renders the main chat interface."""
    st.title(f"👋 Welcome, {st.session_state.full_name}! I'm your HR Assistant.")
    
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
            my_id = f"My Employee id is {st.session_state.employee_id} and my full name is {st.session_state.full_name}."
            #print(my_id)
            new_prompt = f"{my_id} Now {prompt}"
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
    if st.button("Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.session_state.employee_id = None
        st.session_state.full_name = None
        st.rerun()


# def chat_interface_new():
#     st.title(f"👋 Welcome, {st.session_state.full_name}! I'm your HR Assistant.")
#     # Initialize chat history
#     if "messages" not in st.session_state:
#         # print("Creating session state")
#         st.session_state.messages = []

#     # Display chat messages from history on app rerun
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Accept user input
#     if prompt := st.chat_input("What is up?"):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         # Display user message in chat message container
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         # Display assistant response in chat message container
#         with st.spinner("Generating response..."):
#             with st.chat_message("assistant"):
#                 response = invoke_chain(prompt)
#                 st.markdown(response)
#         st.session_state.messages.append({"role": "assistant", "content": response})



def main():
    """The main entry point of the Streamlit application."""
    initialize_session_state()
    print("start")

    # my_id = f"my empoyess id is 1  and my full name Sandeep Bera."
    # print(my_id)
    
    
    # new_prompt = "Get the all leave details of 'Sandeep'."
    # new_prompt2 = "Get the all leave details of 'Gourab'."

    # new_prompt3 = f"{my_id} now {new_prompt}"
    # new_prompt4 = f"{my_id} now {new_prompt2}"



    #print(get_chain_param(new_prompt3))
    #print(get_chain_param(new_prompt4))
    # print(get_chain_param(new_prompt3))
    # print(get_chain_param(new_prompt4))
    # print(get_chain_param(new_prompt3))
    # print(get_chain_param(new_prompt4))
    # print(get_chain_param(new_prompt))
    # print(get_chain_param(new_prompt2))
    # print(get_chain_param(new_prompt))
    # print(get_chain_param(new_prompt2))
    # print(get_chain_param(new_prompt))
    # print(get_chain_param(new_prompt2))
    # invoke_chain(new_prompt )
    # invoke_chain(new_prompt )
    # invoke_chain(new_prompt )
    #x=0

    # Determine which screen to display based on login status
    #login_screen()
    if st.session_state.logged_in:
        chat_interface()
        
    else:
        #chat_interface()
        login_screen()

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











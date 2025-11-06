from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.memory import ChatMessageHistory

#from import models
from database import get_db
import os

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

#from table_details import table_chain as select_table
from prompts import  answer_prompt, final_prompt

from dotenv import load_dotenv

#db = get_db()
#print(db.get_usable_table_names())

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")


leave_quota_prompt  = """
Here are the maximum leave quotas permitted for all employees:

*   **Total Annual Leaves (All Types):** You can take a maximum of **30 paid days** of leave in total per year.

This total is divided into the following specific categories:

*   **Annual Leave:** Maximum **15 days** per year.
*   **Sick Leave:** Maximum **10 days** per year.
*   **Casual Leave:** Maximum **5 days** per year.
*   **Unpaid Leave:** There is no strict internal limit on Unpaid Leave (subject to manager approval).
"""

def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        history.add_message(message)
        # if message["role"] == "user":
        #     history.add_user_message(message["content"])
        #     #history.add_message(message)
        # else:
        #     history.add_ai_message(message["content"])
        #     #history.add_message(message)
    return history

def get_chain():
    #print("Creating chain")
    db = get_db()
    print("---------------db----------")
    #########print(db.table_info)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    generate_query = create_sql_query_chain(llm, db, final_prompt, leave_quota_prompt ) 
    #query = generate_query.invoke({"question":"how many employees are"})
    #print(query)
    execute_query = QuerySQLDataBaseTool(db=db)
    #print(execute_query.invoke(query))

    rephrase_answer = answer_prompt | llm | StrOutputParser()
    #chain = generate_query | execute_query
    #print(chain.invoke({"question":"how many employees are there and what are their  employee id"}))
    chain = (
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
    )
    print("-------------gourav-------------")
    #response = chain.invoke({"question":f"my name is gourab. find  how many  leaves   I  have  taken. "})
    return chain

def invoke_chain(question,messages):
    chain = get_chain()
    print("-----------chain------------")
    #print(chain.invoke({"question":question}))
    history = create_history(messages)
    print("-----------messages history------------")
    print(history.messages)
    response = chain.invoke({"question": question,"top_k":20,"messages":history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    #response = chain.invoke({"question": question})
    #print(response)
    return response

#get_chain()

""" def get_chain_param(question):
    #print("Creating chain")
    db = get_db()
    print("---------------db----------")
    #########print(db.table_info)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    print("---------------db0----------")
    generate_query = create_sql_query_chain(llm, db, final_prompt ) 
    print("---------------db1----------")
    #query = generate_query.invoke({"question":"how many employees are there"})
    print("---------------db2----------")
    print("---------------query----------")
    #########print(query)
    execute_query = QuerySQLDataBaseTool(db=db)
    #print(execute_query.invoke(query))

    rephrase_answer = answer_prompt | llm | StrOutputParser()
    #chain = generate_query | execute_query
    #print(chain.invoke({"question":"how many employees are there and what are their  employee id"}))
    chain = (
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
    )
    print("-------------get chain param-------------")
    response = chain.invoke({"question":question})
    return response """
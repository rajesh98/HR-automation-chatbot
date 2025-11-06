################# NOT USED FOR NOW. GIVING ERRORS IN CHROMA DB
examples = [     
    {
        "input": "List all Employess",
        "query": "SELECT * FROM employees;"
    },
    {
        "input": "Get the all leave details of 'Sandeep'.",
        "query": "select * from leave_transactions join employees on leave_transactions.employee_id = employees.employee_id  where employees.full_name like '%Sandeep%'; "
    }
]

from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
import streamlit as st

@st.cache_resource
def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        Chroma,
        k=1,
        input_keys=["input"],
    )
    ####print("----------select eg----------")
    #########print(example_selector.select_examples({"input": "Get the all leave details of 'Sandeep'."}))
    return example_selector
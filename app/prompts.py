
from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from database import get_db



# db = get_db()
# table_info = db.get_usable_table_names()

examples = [
    {
        "input": "List all Employess",
        "query": "SELECT * FROM employees;"
    },
    {
        "input": "Get the all leave details of 'Sandeep'.",
        "query": "SELECT * from leave_transactions join employees on leave_transactions.employee_id = employees.employee_id  where employees.full_name like '%Sandeep%'; "
    },
    {
        "input": "List all Employess which are working under 'Sandeep Bera'.",
        "query": "SELECT * FROM employees WHERE manager_employee_id = (SELECT employee_id FROM employees WHERE full_name = 'Sandeep Bera');"
    },
    {
        "input": "List all Employess who consider 'Sandeep Bera' as manager.",
        "query": "SELECT * FROM employees WHERE manager_employee_id = (SELECT employee_id FROM employees WHERE full_name = 'Sandeep Bera');"
    },
    {
        "input": "My Employee id is 1. List all Employess working under me",
        "query": "SELECT * FROM employees e WHERE e.manager_employee_id = 1"
    },
    {
        "input": "List all managers in the organization'",
        "query": "SELECT * from employees e where e.role = 'manager';"
    },
    {
        "input": "My Employee id is 1. List all leaves taken by Employess working under me",
        "query": "SELECT * from leave_transactions lt join employees e on e.employee_id = lt.employee_id where e.manager_employee_id = 1;"
    },
    {
        "input": "My Employee id is 2. Who is my manager or to  whom will i report.",
        "query": "SELECT * from employees e where e.employee_id = (SELECT manager_employee_id from employees where employee_id = 2)"
    },
    {   "input": "My Employee id is 2. Apply a sick leave for me on 11 July,2025.",
        "query": "INSERT INTO leave_transactions (employee_id, leave_date, leave_type) VALUES (2, '2025-06-11', 'Sick Leave');"
    },
    {   "input": "My Employee id is 2. Apply a Gneral leave for me on 11 July,2025.",
        "query": "INSERT INTO leave_transactions (employee_id, leave_date, leave_type) VALUES (2, '2025-06-11', 'General Leave');"
    },
    {
       "input": "My Employee id is 2. Apply a Casual leave for me on 11 July,2025.",
        "query": "INSERT INTO leave_transactions (employee_id, leave_date, leave_type) VALUES (2, '2025-06-11', 'Casual Leave');"
    },
    {
       "input": "My Employee id is 2. Apply a leave for me on 11 July,2025.",
        "query": "INSERT INTO leave_transactions (employee_id, leave_date) VALUES (2, '2025-06-11');"
    },
    {
       "input": "My Employee id is 2. How many more leaves available for me",
        "query": "SELECT 30 - count(*) from leave_transactions where employee_id = 2 ;"
    },
    {
       "input": "My Employee id is 2. How many more leaves can I take",
        "query": "SELECT 30 - count(*) from leave_transactions where employee_id = 2 ;"
    },
    {
       "input": "My Employee id is 2. what is my leave balance",
        "query": "SELECT 30 - count(*) from leave_transactions where employee_id = 2 ;"
    },
]


example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    #example_selector=get_example_selector(),
    examples=examples,
    input_variables=["input","top_k"],
)
print("-----------after eg selector---------------")
print(few_shot_prompt.format(input="Get the all leave details of 'Sandeep'."))

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a MySQL expert. Given an input question, create a syntactically correct Postgres SQL query to run, do not include any markdown syntax (```sql).Only give the SQL so that it is directly executed in the DataBase.Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
        few_shot_prompt,
        #MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)
print("------------final -promppt------------")
#######print(final_prompt.format(input = "Leaves details of sandeep?", table_info = "s t i"))

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

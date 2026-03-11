
from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from database import get_db



# db = get_db()
# table_info = db.get_usable_table_names()
# 
examples = [
{
"input": "List first 100 Devices",
"query": 'SELECT * FROM "Device" ORDER BY id ASC LIMIT 100'
},
{
"input": "How many Devices are there available?",
"query": 'SELECT COUNT(*) FROM "Device"'
},
{
"input": "How many Devices active/down?",
"query": '''
    SELECT
    COUNT(CASE WHEN last_report >= (SELECT MAX(timestamp) FROM "DeviceHealth") - INTERVAL '1 hour' THEN 1 END) AS active_count,
    COUNT(CASE WHEN last_report < (SELECT MAX(timestamp) FROM "DeviceHealth") - INTERVAL '1 hour' OR last_report IS NULL THEN 1 END) AS down_count
    FROM (
    SELECT d."deviceId", MAX(dh.timestamp) AS last_report
    FROM "Device" d
    LEFT JOIN "DeviceHealth" dh ON d."deviceId" = dh."deviceId"
    GROUP BY d."deviceId"
    ) status;
        '''
},
{
"input": "details of down devices",
"query": '''
        SELECT d."deviceId", d.model, d.manufacturer, COALESCE(to_char(max_ts.last_seen, 'YYYY-MM-DD HH24:MI:SS'), 'Never Reported') as last_seen
        FROM "Device" d
        LEFT JOIN (
        SELECT "deviceId", MAX(timestamp) as last_seen
        FROM "DeviceHealth"
        GROUP BY "deviceId"
        ) max_ts ON d."deviceId" = max_ts."deviceId"
        WHERE max_ts.last_seen IS NULL
        OR max_ts.last_seen < (SELECT MAX(timestamp) FROM "DeviceHealth") - INTERVAL '1 hour';
'''
},
{
"input": "Show Details of Devices Health?",
"query": '''
        SELECT d.model, d.manufacturer, dh.*
        FROM "DeviceHealth" dh
        JOIN "Device" d ON dh."deviceId" = d."deviceId"
        ORDER BY dh.timestamp DESC;

'''
},
{
"input": "Show Details of Devices Connectivity measurement?",
"query": '''
        SELECT d.model, d.manufacturer, dc.*
        FROM "DeviceDataConnectivity" dc
        JOIN "Device" d ON dc."deviceId" = d."deviceId"
        ORDER BY dc.timestamp DESC;
'''
},
{
"input": "What are the devices having issue?",
"query": '''
        SELECT DISTINCT d."deviceId", d.model, d.manufacturer
        FROM "Device" d
        LEFT JOIN "DeviceHealth" dh ON d."deviceId" = dh."deviceId"
        LEFT JOIN "DeviceDataConnectivity" dc ON d."deviceId" = dc."deviceId"
        LEFT JOIN "DeviceNetworkSignal" ds ON d."deviceId" = ds."deviceId"
        WHERE dh."cpuUsagePercent" > 85
        OR dh."batteryTempCelsius" > 45
        OR dh."batteryPercent" < 15
        OR (ds."rsrpDbm" < -110 AND CAST(TRIM(TRAILING '%' FROM dc.loss) AS DOUBLE PRECISION) > 5)
        OR CAST(TRIM(TRAILING 'ms' FROM dc."avgDelay") AS DOUBLE PRECISION) > 200;
'''
}
]

""" examples = [
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
        "query": "INSERT INTO leave_transactions (employee_id, leave_date, leave_type) VALUES (2, '2025-06-11', 'sick');"
    },
    {   "input": "My Employee id is 2. Apply a Gneral leave for me on 11 July,2025.",
        "query": "INSERT INTO leave_transactions (employee_id, leave_date, leave_type) VALUES (2, '2025-06-11', 'general');"
    },
    {
       "input": "My Employee id is 2. Apply a Casual leave for me on 11 July,2025.",
        "query": "INSERT INTO leave_transactions (employee_id, leave_date, leave_type) VALUES (2, '2025-06-11', 'casual');"
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
    {
       "input": "My Employee id is 2. How many more general leaves available for me",
        "query": "SELECT (SELECT max_count  from  max_leave_quota where leave_type = 'general') - (SELECT count(*) from leave_transactions where employee_id = 2 and leave_type = 'general');"
    },
    {
       "input": "My Employee id is 2. How many more sick leaves can I take",
        "query": "SELECT (SELECT max_count  from  max_leave_quota where leave_type = 'sick') - (SELECT count(*) from leave_transactions where employee_id = 2 and leave_type = 'sick') ;"
    },
    {
       "input": "My Employee id is 2. what is my vaccation leave balance",
        "query": "SELECT (SELECT max_count  from  max_leave_quota where leave_type = 'vaccation') - (SELECT count(*) from leave_transactions where employee_id = 2 and leave_type = 'vaccation') ;"
    },
    {
       "input": "My Employee id is 2. what is the grievances redressal policy in my company",
        "query": "SELECT policy_details from company_policy where policy_type='grievances_redressal';"
    },
    {
       "input": "My Employee id is 2. what is the recruitment policy in my company",
        "query": "SELECT policy_details from company_policy where policy_type='recruitment';"
    },
    {
       "input": "My Employee id is 2. what is the probation policy in my company",
        "query": "SELECT policy_details from company_policy where policy_type='probation';"
    },
    {
       "input": "My Employee id is 2. what is the attendance policy in my company",
        "query": "SELECT policy_details from company_policy where policy_type='attendance_Leave_Management';"
    },
    {
       "input": "My Employee id is 2. what is the notice period policy in my company",
        "query": "SELECT policy_details from company_policy where policy_type='notice_period';"
    },

] """


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
#---------------print(few_shot_prompt.format(input="Get the all leave details of 'Sandeep'."))

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a postgres sql expert. Given an input question, create a syntactically correct Postgres SQL query to run, do not include any markdown syntax (```sql).Only give the SQL so that it is directly executed in the DataBase.Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
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

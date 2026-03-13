################# NOT USED FOR NOW. GIVING ERRORS IN CHROMA DB
examples = [     
    {
        "input": "List all Employess",
        "query": "SELECT * FROM employees;"
    },
    {
        "input": "Get the all leave details of 'Sandeep'.",
        "query": "select * from leave_transactions join employees on leave_transactions.employee_id = employees.employee_id  where employees.full_name like '%Sandeep%'; "
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
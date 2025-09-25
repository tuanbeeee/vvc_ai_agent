import pyodbc
import json
from google import genai
from google.genai import types
from decimal import Decimal

#-------------------------------------------------------------------------------
# Define a function that the model can call to control smart lights
set_light_values_declaration = {
    "name": "set_light_values",
    "description": "Điều chỉnh độ sáng của đèn và màu sắc của đèn.",
    "parameters": {
        "type": "object",
        "properties": {
            "brightness": {
                "type": "integer",
                "description": "Độ sáng của đèn sẽ từ 0 đến 100. Nếu là 0 thì đèn tắt nếu là 100 thì đèn sáng ở độ sáng lớn nhất",
            },
            "color_temp": {
                "type": "string",
                "enum": ["sáng chói", "lạnh", "ấm"],
                "description": "Màu đèn có thể điều chỉnh được, có thể là 'sáng chói', 'ấm', 'lạnh'.",
            },
        },
        "required": ["brightness", "color_temp"],
    },
}

get_store_sales_information_declaration = {
    "name": "query_sql_server",
    "description": "Lấy thông tin doanh thu tại cửa hàng",
}

data_analysis_to_determine_employee_capacity_declaration = {
    "name": "analysis_data",
    "description": "Phân tích data, sau đó xác định năng lực nhân viên",
    "parameters": {
        "type": "object",
        "properties": {
            "dataT": {
                "type": "string",
                "description": "dataT là doanh thu của cửa hàng dưới dạng json. Trong file json sẽ có trường TotalAmount là doanh thu của nhân viên đang trực ca đó",
            }
        },
        "required": ["dataT"],
    },
}
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This is the actual function that would be called based on the model's suggestion
def set_light_values(brightness: int, color_temp: str) -> dict[str, int | str]:
    return {"brightness": brightness, "colorTemperature": color_temp}

def data_analysis_to_determine_employee_capacity(dataT: str) -> (str):
    print(f"Tool Call: data_analysis_to_determine_employee_capacity")
    return dataT

def get_store_sales_information() -> str:
    print(f"Tool Call: get_store_sales_information")
    """Run stored procedure [dbo].[st_TestAI] and return results as JSON string."""
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost,2529;"
            "DATABASE=POS4UCloud_NA3;"
            "UID=sa;"
            "PWD=123@AaBb;"
        )
        
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.st_TestAI}")

        # Fetch column names
        columns = [col[0] for col in cursor.description]

        # Convert row data (Decimal -> float)
        def convert_value(v):
            if isinstance(v, Decimal):
                return float(v)
            return v

        rows = [
            {col: convert_value(val) for col, val in zip(columns, row)}
            for row in cursor.fetchall()
        ]

        cursor.close()
        conn.close()

        return json.dumps(rows, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)})
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Configure the client and tools
client = genai.Client(api_key="AIzaSyA9dDNjwwfZEpKOw0WUJWi0LJ75Jopz-VA")
tools = types.Tool(
    function_declarations=[
        set_light_values_declaration, 
        get_store_sales_information_declaration,
        data_analysis_to_determine_employee_capacity_declaration
        ]
    )

def run_agent(user_prompt: str) -> str:
    contents = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    config = types.GenerateContentConfig(
        tools=[data_analysis_to_determine_employee_capacity, get_store_sales_information],
        thinking_config=types.ThinkingConfig(thinking_budget=1024)
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config,
    )

    return response.candidates[0].content.parts[0].text
#-------------------------------------------------------------------------------
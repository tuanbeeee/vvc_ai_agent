import pyodbc
import json
from google import genai
from google.genai import types
from decimal import Decimal
import ollama
#-------------------------------------------------------------------------------
<<<<<<< Updated upstream
# This is the actual function that would be called based on the model's suggestion
=======
# Define a function that the model can call to control smart lights
# set_light_values_declaration = {
#     "name": "set_light_values",
#     "description": "Điều chỉnh độ sáng của đèn và màu sắc của đèn.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "brightness": {
#                 "type": "integer",
#                 "description": "Độ sáng của đèn sẽ từ 0 đến 100. Nếu là 0 thì đèn tắt nếu là 100 thì đèn sáng ở độ sáng lớn nhất",
#             },
#             "color_temp": {
#                 "type": "string",
#                 "enum": ["sáng chói", "lạnh", "ấm"],
#                 "description": "Màu đèn có thể điều chỉnh được, có thể là 'sáng chói', 'ấm', 'lạnh'.",
#             },
#         },
#         "required": ["brightness", "color_temp"],
#     },
# }

# get_store_sales_information_declaration = {
#     "name": "get_store_sales_information",
#     "description": "Lấy thông tin doanh thu tại cửa hàng",
# }

# data_analysis_to_determine_employee_capacity_declaration = {
#     "name": "data_analysis_to_determine_employee_capacity",
#     "description": "Phân tích data, sau đó xác định năng lực nhân viên",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "dataT": {
#                 "type": "string",
#                 "description": "dataT là doanh thu của cửa hàng dưới dạng json. Trong file json sẽ có trường TotalAmount là doanh thu của nhân viên đang trực ca đó",
#             }
#         },
#         "required": ["dataT"],
#     },
# }
# #-------------------------------------------------------------------------------

# #-------------------------------------------------------------------------------
# # This is the actual function that would be called based on the model's suggestion
# def set_light_values(brightness: int, color_temp: str) -> dict[str, int | str]:
#     return {"brightness": brightness, "colorTemperature": color_temp}
>>>>>>> Stashed changes

# def data_analysis_to_determine_employee_capacity(dataT: str) -> (str):
#     print(f"Tool Call: data_analysis_to_determine_employee_capacity")
#     return dataT

# def get_store_sales_information() -> str:
#     print(f"Tool Call: get_store_sales_information")
#     """Run stored procedure [dbo].[st_TestAI] and return results as JSON string."""
#     try:
#         conn = pyodbc.connect(
#             "DRIVER={ODBC Driver 17 for SQL Server};"
#             "SERVER=localhost,2529;"
#             "DATABASE=POS4UCloud_NA3;"
#             "UID=sa;"
#             "PWD=123@AaBb;"
#         )
        
#         cursor = conn.cursor()
#         cursor.execute("{CALL dbo.st_TestAI}")

#         # Fetch column names
#         columns = [col[0] for col in cursor.description]

#         # Convert row data (Decimal -> float)
#         def convert_value(v):
#             if isinstance(v, Decimal):
#                 return float(v)
#             return v

#         rows = [
#             {col: convert_value(val) for col, val in zip(columns, row)}
#             for row in cursor.fetchall()
#         ]

#         cursor.close()
#         conn.close()

#         return json.dumps(rows, indent=2, ensure_ascii=False)

#     except Exception as e:
#         return json.dumps({"error": str(e)})
    
# def get_sales_item_information(item_codes: list[str]) -> str:
#     print(f"Tool Call: get_sales_item_information")
#     """
#     Run stored procedure [dbo].[st_TestAICase2] with @ItemCodes parameter (CSV string)
#     and return results as JSON string.
#     """
#     try:
#         conn = pyodbc.connect(
#             "DRIVER={ODBC Driver 17 for SQL Server};"
#             "SERVER=localhost,2529;"
#             "DATABASE=POS4UCloud_NA3;"
#             "UID=sa;"
#             "PWD=123@AaBb;"
#         )
        
#         cursor = conn.cursor()

#         # Convert list -> CSV
#         csv_codes = ",".join(item_codes)

#         # Gọi stored procedure
#         cursor.execute("{CALL dbo.st_TestAICase2 (?)}", (csv_codes,))

#         # Lấy tên cột
#         columns = [col[0] for col in cursor.description]

#         # Convert kiểu Decimal về float
#         def convert_value(v):
#             if isinstance(v, Decimal):
#                 return float(v)
#             return v

#         # Mapping rows -> dict
#         rows = [
#             {col: convert_value(val) for col, val in zip(columns, row)}
#             for row in cursor.fetchall()
#         ]

#         cursor.close()
#         conn.close()

#         return json.dumps(rows, indent=2, ensure_ascii=False)

#     except Exception as e:
#         return json.dumps({"error": str(e)})

# #-------------------------------------------------------------------------------

<<<<<<< Updated upstream
#-------------------------------------------------------------------------------
# Configure the client and tools
client = genai.Client(api_key="AIzaSyA9dDNjwwfZEpKOw0WUJWi0LJ75Jopz-VA")
=======
# #-------------------------------------------------------------------------------
# # Configure the client and tools
# client = genai.Client(api_key="AIzaSyA9dDNjwwfZEpKOw0WUJWi0LJ75Jopz-VA")
# tools = types.Tool(
#     function_declarations=[
#         set_light_values_declaration, 
#         get_store_sales_information_declaration,
#         data_analysis_to_determine_employee_capacity_declaration
#         ] # type: ignore
#     )

# chat_history = []

# # This function now yields chunks of the response
# def run_agent(user_prompt: str):
#     print(user_prompt)
#     global chat_history

#     chat_history.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

#     config = types.GenerateContentConfig(
#         tools=[data_analysis_to_determine_employee_capacity, get_store_sales_information, get_sales_item_information],
#         thinking_config=types.ThinkingConfig(thinking_budget=-1)
#     )

#     # Use the streaming method
#     response_stream = client.models.generate_content_stream(
#         model="gemini-2.5-flash-image-preview",
#         contents=chat_history,
#         config=config,
#     )
    
#     full_response_text = ""
#     # Iterate through the stream and yield text chunks immediately
#     for chunk in response_stream:
#         # Only process text chunks for streaming
#         if chunk.text :  # type: ignore 
#             full_response_text += chunk.text # type: ignore
#             yield chunk.text # type: ignore

#     # IMPORTANT: Update the history with the *complete* response after the stream is done
#     if full_response_text:
#         chat_history.append(types.Content(
#             role="model", 
#             parts=[types.Part(text=full_response_text)]
#         ))
#     #-------------------------------------------------------------------------------
def add_two_numbers(a: int, b: int) -> int:
  """
  Add two numbers

  Args:
    a: The first integer number
    b: The second integer number

  Returns:
    int: The sum of the two numbers
  """
  return a + b

response = ollama.chat(
        messages=[
            {
                'role': 'user', 
                'content': "What is 10 + 10?"
            }
        ],
        model='llama3.1:latest',
        tools=[add_two_numbers], # Actual function reference
    )
    
available_functions = {
  'add_two_numbers': add_two_numbers,
}
>>>>>>> Stashed changes

for tool in response.message.tool_calls or []:
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            print(f'Function output:', function_to_call(**tool.function.arguments))
        else:
            print(f'Function output:', tool.function.name)
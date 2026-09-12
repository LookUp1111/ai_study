from langchain_core.tools import tool
from spark_model import llm
from langchain_core.messages import HumanMessage
# @tool
# def add(a: int, b: int) -> int:
#     """Add two integers.
#
#     Args:
#         a: First integer
#         b: Second integer
#     """
#     return a + b
# [
#   {
#     "type": "function",
#     "function": {
#       "name": "add",
#       "description": "Add two integers.",
#       "parameters": {
#         "type": "object",
#         "properties": {
#           "a": {"type": "integer", "description": "First integer"},
#           "b": {"type": "integer", "description": "Second integer"}
#         },
#         "required": ["a", "b"]
#       }
#     }
#   },
#   {
#     "type": "function",
#     "function": {
#       "name": "multiply",
#       "description": "Multiply two integers.",
#       "parameters": { /* 同上 */ }
#     }
#   }
# ]


@tool
def add(a:int,b:int) -> int:
    """
    将两个整数相加。

    参数：
    a: 第一个整数
    b: 第二个整数
    """
    return a + b

@tool
def multiply(a:int,b:int) -> int:
    """
    把两个整数乘起来。
     参数：
    a: 第一个整数
    b: 第二个整数
    """
    return  a * b

import  json
llm_with_tools = llm.bind_tools([add,multiply])

query = "2的4倍是多少？"
messages = [HumanMessage(content=query)]
# print(messages)

ai_msg = llm_with_tools.invoke(messages)

# print(ai_msg)
messages.append(ai_msg)
# print(messages)
available_tools = {"add": add, "multiply": multiply}
# print(available_tools)
for tool_call in ai_msg.tool_calls:
    selected_tool = available_tools[tool_call["name"].lower()]
    print(selected_tool)
    tool_msg = selected_tool.invoke(tool_call)
    print(tool_msg)
    messages.append(tool_msg)

new_output = llm_with_tools.invoke(messages)
for message in messages:
    msg_dict = message.model_dump()
    print(json.dumps(msg_dict, indent=4, ensure_ascii=False))
print(new_output.content)

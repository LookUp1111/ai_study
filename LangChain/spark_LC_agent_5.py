from spark_model import llm
from langchain_core.prompts import PromptTemplate
json_schema = {
    "title": "Date",
    "description": "Formated date expression",  # 注意：英文拼写应为 "Formatted"
    "type": "object",
    "properties": {
        "year": {
            "type": "integer",
            "description": "year, YYYY",
        },
        "month": {
            "type": "integer",
            "description": "month, MM",
        },
        "day": {
            "type": "integer",
            "description": "day, DD",
        },
        "era": {
            "type": "string",
            "description": "BC or AD",
        },
    },
}

structured_llm = llm.with_structured_output(json_schema)

#定义提示词
template = """提取用户输入中的日期。
要求：
- 月份请转换为数字（1-12）
- 如果是公元后，era 填 "AD"；如果是公元前，era 填 "BC"
- 严格按照给定的JSON结构输出
用户输入：
{query}"""
#PromptTemplate 初始化
prompt = PromptTemplate.from_template(
    template,
)

query = "2023年四月6日天气晴"

input_prompt = prompt.format_prompt(query=query)

ret = llm.invoke(input_prompt)

print(ret)

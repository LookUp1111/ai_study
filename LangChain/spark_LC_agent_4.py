from pydantic import BaseModel,Field
#定义输出对象
class Date(BaseModel):
    year: int = Field(description="Year")
    month: int = Field(description="Month")
    day: int = Field(description="Day")
    era: str = Field(description="Era, must be 'BC' or 'AD'")

# {
#   "title": "Date",
#   "type": "object",
#   "properties": {
#     "year": {
#       "title": "Year",
#       "description": "Year",
#       "type": "integer"
#     },
#     "month": {
#       "title": "Month",
#       "description": "Month",
#       "type": "integer"
#     },
#     "day": {
#       "title": "Day",
#       "description": "Day",
#       "type": "integer"
#     },
#     "era": {
#       "title": "Era",
#       "description": "BC or AD",
#       "type": "string"
#     }
#   },
#   "required": ["year", "month", "day", "era"]
# }

from spark_model import llm
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,HumanMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

#定义结构化输出类型
structured_llm = llm.with_structured_output(Date)
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

ret = structured_llm.invoke(input_prompt)
print("类型:", type(ret))
print("解析结果:", ret)
print(f"年: {ret.year}, 月: {ret.month}, 日: {ret.day}, 纪元: {ret.era}")
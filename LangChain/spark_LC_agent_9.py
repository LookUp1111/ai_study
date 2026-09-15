from langchain_core.prompts import  ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
from spark_model import llm
import json

class SortEnum(str,Enum): #规定排序字段只能是按流量（data）或价格（price）
    data = 'data'
    price = 'price'

class OrderingEnum(str,Enum): #规定排序方式只能是升序（ascend）或降序（descend）
    ascend = 'ascend'
    descend = 'descend'

#定义输出结构
class Semantics(BaseModel):
    name:Optional[str] = Field(description="流量包名称",default=None) #Optional[str]是可选字符串 Field(description="...")告诉大模型要提取的字段 default=None 大模型没找到可提取的字段返回None
    price_lower:Optional[int] = Field(description="价格下限",default=None)
    price_upper:Optional[int] = Field(description="价格上限",default=None)
    data_lower:Optional[int] = Field(description="流量下限",default=None)
    data_upper:Optional[int] = Field(description="流量上限",default=None)
    sort_by:Optional[SortEnum] = Field(description="案价格或流量排序",default=None)
    ordering:Optional[OrderingEnum] = Field(description="升序或降序排序",default=None)

    @field_validator("ordering", mode="before")
    @classmethod
    def fix_ordering(cls, v):
        if isinstance(v, str):
            v = v.replace(" ", "").lower()  # "desc end" -> "descend"
        return v

    @field_validator("sort_by", mode="before")
    @classmethod
    def fix_sort_by(cls, v):
        if isinstance(v, str):
            v = v.replace(" ", "").lower()
        return v
#定义输出结构2
SYSTEM = """你是一个语义解析器。只输出 JSON，不要任何解释或多余文字。
必须严格使用以下字段名和结构，不要自创字段：
{{
  "name":        "流量包名称，没有填 null",
  "price_lower": "价格下限整数，没有填 null",
  "price_upper": "价格上限整数，没有填 null",
  "data_lower":  "流量下限整数(GB)，没有填 null",
  "data_upper":  "流量上限整数(GB)，没有填 null",
  "sort_by":     "只能是 'data' 或 'price'，没有填 null",
  "ordering":    "只能是 'ascend' 或 'descend'，没有填 null"
}}

示例：
输入：不超过100元的流量大套餐有哪些
输出：{{"name":null,"price_lower":null,"price_upper":100,"data_lower":null,"data_upper":null,"sort_by":"data","ordering":"descend"}}

输入：50到100元之间50GB以上的套餐，按价格从低到高
输出：{{"name":null,"price_lower":50,"price_upper":100,"data_lower":50,"data_upper":null,"sort_by":"price","ordering":"ascend"}}
"""

#prompt模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个语义解析器。你的任务是将用户的输入解释成JSON表示，不要回答用户的问题。"),
        ("human","{text}")
    ]
)
prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system",SYSTEM),
        ("human","{text}")
    ]
)


#with_structured_outout把pydantic类Semantics转换为OpenAI的 Function Calling 或 JSON Mode 的格式大模型返回的不再是一段文本，而是自动被解析并验证为一个 Semantics 类的实例对象。
structures_llm = llm.with_structured_output(Semantics,method="json_mode")

#LCEL 表达式
runnable = (
    {"text":RunnablePassthrough()}|prompt|structures_llm
)
runnable2 = (
    {"text":RunnablePassthrough()}|prompt2|structures_llm
)


#正常输出
out = (prompt | llm).invoke({"text": "不超过100元的流量大套餐有哪些"})
print(out.content)
print("*****"*23)

#格式化输出
ret = runnable.invoke("不超过100元的流量大套餐有哪些")
print(
    json.dumps(
        ret.model_dump(),
        indent = 4,
        ensure_ascii= False
    )
)

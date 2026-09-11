import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv() #加载 .env
key = os.getenv("SPARK_API_KEY") #获得api_key

#封装模型
llm = ChatOpenAI(
    api_key = key,
    base_url = "https://maas-api.cn-huabei-1.xf-yun.com/v2",
    model = "spark-x2.5-4b",
)

# response = llm.invoke("你是谁")
# print(response.content)

#多轮对话Session封装
from langchain_core.messages import (
    AIMessage,  # 等价于OpenAI接口中的assistant role
    HumanMessage, # 等价于OpenAI接口中的user role
    SystemMessage, # 等价于OpenAI接口中的system role
)

messages = [
    SystemMessage(content="你是AGIClass的课程助理"),
    HumanMessage(content="我是学员，我叫李明"),
    AIMessage(content="欢迎"),
    HumanMessage(content="我是谁"),
]

ret = llm.invoke(messages)
print(ret.content)
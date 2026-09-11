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

response = llm.invoke("你是谁")
print(response.content)

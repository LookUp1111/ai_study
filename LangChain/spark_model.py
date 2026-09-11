import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
api_key = os.getenv("SPARK_API_KEY")
api_url = "https://maas-api.cn-huabei-1.xf-yun.com/v2"
llm = ChatOpenAI(
    api_key = api_key,
    base_url = api_url,
    model = "spark-x2.5-4b",
)
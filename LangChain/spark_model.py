import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
api_key = os.getenv("SPARK_API_KEY")
api_url = "https://maas-api.cn-huabei-1.xf-yun.com/v2"
api_key2 = os.getenv("DEEPSEEK_API_KEY")
api_url2  = "https://api.deepseek.com"
llm = ChatOpenAI(
    api_key = api_key,
    base_url = api_url,
    model = "spark-x2.5-4b",
    temperature=0,
)

llm_DP_chat = ChatOpenAI(
    api_key = api_key2,
    base_url = api_url2,
    model = "deepseek-chat",
    temperature=0,
)

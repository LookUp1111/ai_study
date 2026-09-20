from llama_index.llms.openai_like import OpenAILike
import os
from dotenv import load_dotenv

from llama_index.core import PromptTemplate
#定义提示词模板
prompt = PromptTemplate("写一个关于{topic}的笑话")
#prompt.format(topic="小明")

load_dotenv()
api_key = os.getenv("SPARK_API_KEY")
llm = OpenAILike(
    api_key=api_key,
    api_base="https://maas-api.cn-huabei-1.xf-yun.com/v2",
    model="spark-x2.5-4b",
    context_window=8192,
    temperature=0,
    is_chat_model=True
)

response = llm.complete(prompt.format(topic="南瓜"))
print(response.text)
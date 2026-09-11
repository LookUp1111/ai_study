from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.utilities import SerpAPIWrapper

load_dotenv() #加载 。env
api_key = os.getenv("SPARK_API_KEY")
prompt = os.getenv("system_prompt_s")

#定义llm
llm = ChatOpenAI(
    temperature = 0,
    api_key = api_key,
    base_url = "https://maas-api.cn-huabei-1.xf-yun.com/v2",
    model = "spark-x2.5-4b",
)

#获取天气的工具
def get_weather(city: str) -> str:
    """获取指定城市的当前天气状况。
    Args:
        city:要查询天气信息的城市名称。
    """
    return f"It's always sunny in {city}!"

agent = create_agent(
    model= llm,
    tools=[get_weather],
    system_prompt=prompt, #模型上下文
    checkpointer=InMemorySaver(), #短期记忆
)

thread_config = {"configurable":{"thread_id":"1"}}


def get_res(txt):
    result= agent.invoke(
        {"messages": [{"role": "user", "content":txt}]},
        thread_config,
    )

    return result["messages"][-1].content


while True:
    int_txt = input("输入:")
    if int_txt == "1":
        print("（轻轻挥手，眼里带着灿烂的笑意）好呀，再见啦！祝你每天都开开心心，要是之后有有趣的事儿想分享，随时来找我哦，我一直在的～ 😊")
        break
    print(get_res(int_txt))
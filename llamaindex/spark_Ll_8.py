from llama_index.llms.openai_like import OpenAILike
from llama_index.core.llms import ChatMessage,MessageRole
from llama_index.core import ChatPromptTemplate

import os
from dotenv import load_dotenv

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

chat_text_qa_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content="你叫{name},你必须根据用户提供的上下文回答问题",

    ),
    ChatMessage(
        role=MessageRole.SYSTEM,
        content=(
            "已知上下文：\n"
            "{context}\n\n"
            "问题：{question}"),
    )

]

text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

messages =text_qa_template.format_messages(
    name="李四",
    context="这是一个测试",
    question="你是谁，你能干什么"
)
# print(text_qa_template)

rep = llm.chat(messages)
print(rep.message.content)
messages.append(rep.message)
messages.append(ChatMessage(role=MessageRole.USER, content="今天的天气如何"))
rep2 = llm.chat(messages)
print(rep2)
from spark_model import llm
from langchain_core.prompts import (
    ChatPromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder
)

human_prompt = "把你回答的答案改成{language}"
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)

chat_prompt = ChatPromptTemplate.from_messages(
    [MessagesPlaceholder("history"),
     human_message_template]
)

from langchain_core.messages import (
    AIMessage, #大模型的回复
    HumanMessage #用户的提问
                                     )

#手动创建对话历史
human_message = HumanMessage(
    content="埃隆·马斯克是谁？"
)
ai_message = AIMessage(
    content="埃隆·马斯克是一位亿万富翁企业家、发明家和工业设计师"
)
# 对 "history" 和 "language" 赋值
messages = chat_prompt.format_prompt(
    history=[human_message,ai_message],
    language="英文",
)
print(messages.to_messages())
ret = llm.invoke(messages)
print(ret.content)
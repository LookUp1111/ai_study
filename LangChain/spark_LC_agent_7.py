

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    trim_messages,
)
from langchain_core.messages.utils import count_tokens_approximately

#对话历史剪切
messages = [
    SystemMessage(content="you're a good assistant, you always respond with a joke."),
    HumanMessage(content="i wonder why it's called langchain"),
    AIMessage(content="Well, I guess they thought ..."),
    HumanMessage(content="and who is harrison chasing anyways"),
    AIMessage(content="Hmmm let me think ..."),
    HumanMessage(content="what do you call a speechless parrot"),
]

trimmed_messages = trim_messages(
    messages,
    max_tokens=45, #token的数量
    strategy="last", #从后开始数token
    token_counter=count_tokens_approximately, #
    include_system=True, #一定保留system的对话

)
for message in trimmed_messages:

    print(message.content)
def a():
    return 
#可以给对话打标签用filter_messages 筛选
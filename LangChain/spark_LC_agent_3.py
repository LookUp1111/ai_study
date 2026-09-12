from spark_model import llm
from langchain_core.prompts import PromptTemplate

#从文件中加载Prompt
# with open("example_prompt.txt","r",encoding="utf-8") as f:
#     template_str = f.read()
# template = PromptTemplate.from_template(template_str)
#从文件中加载Prompt
template = PromptTemplate.from_file("example_prompt.txt",encoding="utf-8")

print(template)
t1= template.format(topic="黑色幽默")
print(t1)
t2 = llm.invoke(t1)
print(t2.content)
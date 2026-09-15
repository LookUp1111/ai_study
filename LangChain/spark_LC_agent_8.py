# from langchain_core.prompts import PromptTemplate
# from spark_model import llm
# from langchain_core.runnables import  RunnablePassthrough
# from langchain_core.output_parsers import  StrOutputParser
# prompt = PromptTemplate.from_template("讲一个关于{topic}的笑话")
# runnable = (
#     {"topic":RunnablePassthrough()} | prompt | llm | StrOutputParser()
# )
#
# #流式输出
# for s in runnable.stream("小明"):
#     print(s,end="",flush=True)
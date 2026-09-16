from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn
from spark_model import llm

app =FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

prompt = ChatPromptTemplate.from_template("讲一个关于{topic}的笑话")


add_routes(
    app,
    prompt | llm,
    path="/joke"
)

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=9999) #http://localhost:9999/joke/playground/



#netstat -ano | findstr :9999
#taskkill /PID 8452 /F
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader, Settings
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.readers.file import PyMuPDFReader
import os
from dotenv import load_dotenv
from llama_index.embeddings.dashscope import DashScopeEmbedding
from llama_index.llms.openai_like import OpenAILike

load_dotenv()
api_key=os.getenv("ALI_API_KEY")
Settings.embed_model = DashScopeEmbedding(
    model_name="text-embedding-v3",
    api_key=api_key,
    embed_batch_size=6

)

Settings.llm = OpenAILike(
    model="spark-x2.5-4b",
    api_key=os.getenv("SPARK_API_KEY"),
    api_base="https://maas-api.cn-huabei-1.xf-yun.com/v1",
    is_chat_model=True,
    is_function_calling_model=False,
    timeout=120,

)


#加载pdf
documents = SimpleDirectoryReader(
    "./data",
    required_exts=[".pdf"],
    file_extractor={".pdf":PyMuPDFReader()},
).load_data()


#定义Node Parser
node_parser = TokenTextSplitter(chunk_size=300,chunk_overlap=100)
# 切分文档
nodes = node_parser.get_nodes_from_documents(documents)
if __name__=="__main__":


    # 构建index
    index = VectorStoreIndex(nodes)

    # 获取retriever
    vector_retriever = index.as_retriever(
        similarity_top_k=5,  # 返回2个结果
    )

    # 检索
    results = vector_retriever.retrieve("Llama2有多少个参数")

    print(results[0].text)
    print("+++++"*6)
    print(results[1].text)

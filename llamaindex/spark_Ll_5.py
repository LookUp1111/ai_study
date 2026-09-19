import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.end =time.time()
        self.interval = self.end - self.start
        print(f"耗时{self.interval*1000}ms")


from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext

from dotenv import load_dotenv
import os
from llama_index.embeddings.dashscope import DashScopeEmbedding
from llama_index.core import Settings
load_dotenv()
api_key = os.getenv("ALI_API_KEY")
Settings.embed_model = DashScopeEmbedding(
    model_name= "text-embedding-v3",
    api_key=api_key,
    embed_batch_size=6,
)



from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader


client = QdrantClient(location=":memory:") #使用内存模式
collection_name = "ingestion_demo" #创建名为ingestion_demo

collection = client.create_collection(
    collection_name = collection_name,
    #向量维度是1024 距离用余弦相识度
    vectors_config = VectorParams(size=1024,distance=Distance.COSINE)
)

vector_store = QdrantVectorStore( #把Qdrant包装成llamaindex可用向量存储
    client=client,
    collection_name=collection_name,
)


from llama_index.llms.dashscope import DashScope
Settings.llm = DashScope( # 指定TitleExtractor()的标题生成模型
    model_name="qwen-plus",
    api_key=os.getenv("ALI_API_KEY"),
)

pipeline = IngestionPipeline( #按顺序处理文档
    transformations=[
        #把长文档切分成小块 每块300token 相邻重叠100token
        SentenceSplitter(chunk_size=300,chunk_overlap=100),
        #为每个Node生成标题 写入metadata
        TitleExtractor(),
        #为每个Node生成向量 的模型
        Settings.embed_model,
    ],
    #流水运行后会把向量的节点写入Qdrant
    vector_store=vector_store,
)

documents = SimpleDirectoryReader(
    "./data",
    required_exts=[".pdf"],
    file_extractor={".pdf":PyMuPDFReader()},

).load_data() #返回Document列表

#计时
with Timer():
    pipeline.run(documents=documents)

#从向量数据库创建索引，不会重新嵌入文档
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=Settings.embed_model, #指定模型
)

#获取retriever
vector_retriever = index.as_retriever(similarity_top_k=1) #创建检索器，返回一个

#检索 把查询文本作embedding 再到Qdrant中搜索最相似的点
results = vector_retriever.retrieve("网络层的考点")

print(results[0])


#本地包存 缓存
pipeline.persist("./pipeline_storage")
new_pipeline = IngestionPipeline( #按顺序处理文档
    transformations=[
        #把长文档切分成小块 每块300token 相邻重叠100token
        SentenceSplitter(chunk_size=300,chunk_overlap=100),
        #为每个Node生成标题 写入metadata
        TitleExtractor(),
        #为每个Node生成向量 的模型
        Settings.embed_model,
    ],
)

#加载缓存
new_pipeline.load("./pipeline_storage")
with Timer():
    nodes = new_pipeline.run(documents=documents)

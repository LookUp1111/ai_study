from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance

EMBEDDING_DIM = 1024 #存入向量维度
COLLECTION_NAME = "full_demo" #表名
PATH = "./qdrant_db" #定义本地数据持久化的存储路径

client = QdrantClient(path=PATH)

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file import PyMuPDFReader
from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.chat_engine import CondenseQuestionChatEngine


# 1. 指定全局LLM与embedding模型
from dotenv import load_dotenv
from llama_index.embeddings.dashscope import DashScopeEmbedding
from llama_index.llms.openai_like import OpenAILike
import os
load_dotenv()
Settings.llm = OpenAILike(
    model="spark-x2.5-4b",
    api_key=os.getenv("SPARK_API_KEY"),
    api_base="https://maas-api.cn-huabei-1.xf-yun.com/v1",
    is_chat_model=True,
    is_function_calling_model=False,
    timeout=120,
)

Settings.embed_model = DashScopeEmbedding(
    model_name="text-embedding-v3",
    api_key=os.getenv("ALI_API_KEY"),
    embed_batch_size=6,
)

#2. 指定全局文档处理的 Ingestion Pipeline
Settings.transformations=[SentenceSplitter(
    chunk_size=300, #每个文本300token
    chunk_overlap=100, #重叠100token
)]
#3.加载本地文档
documents = SimpleDirectoryReader(
    "./data",
    file_extractor={".pdf":PyMuPDFReader()}
).load_data()

if client.collection_exists(collection_name=COLLECTION_NAME):
    client.delete_collection(collection_name=COLLECTION_NAME)

#4.创建collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE, #距离度量方式为余弦相似度 (Distance.COSINE)
    )

)

#5. 创建 Vector Store
vector_store = QdrantVectorStore(client=client, #将之前创建的 Qdrant client 封装成 LlamaIndex 认识的 QdrantVectorStore 对象
                                 collection_name=COLLECTION_NAME, #
                                 )

# 6. 指定 Vector Store 的 Storage 用于 index
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
) #使用 StorageContext 指定存储上下文（即向量存到 Qdrant 中)

index = VectorStoreIndex.from_documents(
    documents,storage_context=storage_context
) #VectorStoreIndex.from_documents 会自动执行以下流程：文档分块（由 Settings.transformations 控制） -> 调用 OpenAI 计算 Embedding -> 存入 Qdrant

#7.定义检索后排序模型 重排序 (Reranker)：使用 BAAI/bge-reranker-large 模型。它的作用是：在初步向量检索出结果后，对这些结果进行精细打分，最终只保留最相关的 top_n=2 个文档片段。这能大幅提高 RAG 的精度。
from llama_index.postprocessor.dashscope_rerank import DashScopeRerank
reranker = DashScopeRerank(
    model="gte-rerank",
    top_n=2,
    api_key=os.getenv("ALI_API_KEY")
)


#定义RAG Fusion 检索器 它不是只用用户的一个问题去检索，而是利用 LLM 基于原问题生成 3 个不同角度的相似问题 (num_queries=3)。每个问题各召回 5 个结果 (similarity_top_k=5)，最后将这些结果融合去重，再交给 Reranker 排序。
fusion_retriever = QueryFusionRetriever(
    [index.as_retriever()],
    similarity_top_k=5,  # 检索召回 top k 结果
    num_queries=3, # 生成 query 数
    use_async=False, #是为了避免在本地 Qdrant 模式下发生并发写入锁冲突，建议保持。
)
# 9. 构建单轮 query engine
query_engine = RetrieverQueryEngine.from_args(
    fusion_retriever,
    node_postprocessors=[reranker],
)
# 10. 对话引擎
chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine,
)
# 11. 调用进行提问
response = chat_engine.chat("你的问题是什么？比如：这篇文档主要讲了什么？")
print(response)

# 12. 释放资源
client.close()


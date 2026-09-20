from qdrant_client import QdrantClient

EMBEDDING_DIM = 1024
COLLECTION_NAME = "full_demo"
PATH = "./qdrant_db"

# 1. 连接本地 Qdrant (注意：这步不要删)
client = QdrantClient(path=PATH)

from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.chat_engine import CondenseQuestionChatEngine

# 2. 配置全局 LLM 和 Embedding 模型 (必须保留，检索时还要用 Embedding 向量化你的提问)
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

# 3. 绑定已有的 Vector Store (不要再去读取和切分 PDF)
vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)

# 4. ⚠️ 核心替换：直接从已有的向量库加载索引 (不再调用 from_documents)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context
)



# 6. 定义检索器
fusion_retriever = QueryFusionRetriever(
    [index.as_retriever()],
    similarity_top_k=5,
    num_queries=3,
    use_async=False,
)

# 7. 构建查询引擎
query_engine = RetrieverQueryEngine.from_args(
    fusion_retriever,
)

# 8. 对话引擎
chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine,
)

# 9. 提问
print("系统已就绪，输入 exit 退出。")
while True:
    q = input("\n你: ")
    if q.lower() in ["exit", "quit", "退出"]:
        break
    response = chat_engine.chat(q)
    print(f" AI: {response}")

# 10. 释放资源 (解决 msvcrt 报错)
client.close()
print("\n资源已释放，程序退出。")
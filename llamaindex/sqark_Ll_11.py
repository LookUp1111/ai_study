import os
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
)
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.readers.file import PyMuPDFReader
from llama_index.embeddings.dashscope import DashScopeEmbedding
from llama_index.llms.openai_like import OpenAILike

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from llama_index.vector_stores.qdrant import QdrantVectorStore

load_dotenv()

Settings.embed_model = DashScopeEmbedding(
    model_name="text-embedding-v3",
    api_key=os.getenv("ALI_API_KEY"),
    embed_batch_size=6,
)

Settings.llm = OpenAILike(
    model="spark-x2.5-4b",
    api_key=os.getenv("SPARK_API_KEY"),
    api_base="https://maas-api.cn-huabei-1.xf-yun.com/v1",
    is_chat_model=True,
    is_function_calling_model=False,
    timeout=120,
)

documents = SimpleDirectoryReader(
    "./data", required_exts=[".pdf"],
    file_extractor={".pdf": PyMuPDFReader()},
).load_data()

nodes = TokenTextSplitter(chunk_size=512, chunk_overlap=64)\
    .get_nodes_from_documents(documents)

client = QdrantClient(location=":memory:")
collection_name = "demo"
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)

qa_engine = index.as_query_engine()
print(qa_engine.query("网络层的考点有多少个参数？"))
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance

from spark_Ll_3 import nodes

#初始化 Qdrant
client = QdrantClient(location=":memory:") #在内存中启动一个Qdrant实例
collection_name = "demo"  #创建一个名为"demo"的集合
collection = client.create_collection(
    collection_name = collection_name,
    vectors_config = VectorParams(size=1024,distance=Distance.COSINE),
    #size向量维度  Distance.COSINE使用余弦相似度来衡量向量间的距离
)

#将Llamaindex与Qdrant客户端绑定
vector_store = QdrantVectorStore(client=client,collection_name=collection_name)
#创建一个存储上下文，告诉 LlamaIndex 将数据存放在刚才定义的 Qdrant 向量库中
storage_context = StorageContext.from_defaults(vector_store=vector_store)
#创建 index: 通过 Storage Context 关联到自定义的 Vector Store过传入 nodes，LlamaIndex 会自动将文本转化为向量（Embeddings），并存入 Qdrant。
index = VectorStoreIndex(nodes,storage_context=storage_context)
#获得retrierver  as_retriever(similarity_top_k=2)将索引转化为检索器，并设置每次查询返回相似度最高的前 2 个结果（Top-K = 2）
vector_retriever = index.as_retriever(similarity_top_k=5)
#检索 执行自然语言查询
results = vector_retriever.retrieve("网络层的考点")

# if __name__=="__main__":
#     print(results[0])
#     print("___" * 22)
#     for i, node in enumerate(results):
#         print(f"[{i}]{node.text}\n")


# #生成回复
# #单轮问答（Query Engine）
# qa_engine = index.as_query_engine()
# response = qa_engine.query("网络层的考点有多少个？")
# print(response)
# print("++++"*23)
#
# #流式输出
# qa_engine = index.as_query_engine(streaming=True,)
# response = qa_engine.query("网络层的考点有多少个？")
# print(response)
# print("++++"*23)

# #多轮对话 自带上下文
# chat_engine = index.as_chat_engine()
# response = chat_engine.chat("网络层的考点有多少个？")
# print(response)
# response = chat_engine.chat("你总结一下")
# print(response)

#流式输出
chat_engine = index.as_chat_engine()
streaming_response = chat_engine.stream_chat("网络层的考点有多少个？")

for token in streaming_response.response_gen:
    print(token,end="",flush=True)
from llama_index.core import Document
from llama_index.core.node_parser import TokenTextSplitter
from spark_Ll import documents
node_parser = TokenTextSplitter(
    chunk_size=100, #每个chunk的最大长度
    chunk_overlap=50, #chunk之间重叠长度
)

nodes = node_parser.get_nodes_from_documents(
    documents,show_progress=False
)
if __name__=="__name__":
    print(nodes[0].json())


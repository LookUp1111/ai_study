from llama_index.core import Document
from jn_show import show_json
from llama_index.core.node_parser import TokenTextSplitter
from spark_Ll import documents
import json
node_parser = TokenTextSplitter(
    chunk_size=100, #每个chunk的最大长度
    chunk_overlap=50, #chunk之间重叠长度
)

nodes = node_parser.get_nodes_from_documents(
    documents,show_progress=False
)
if __name__=="__main__":
    print(nodes[0].json())
    print(show_json(nodes[0].json()))



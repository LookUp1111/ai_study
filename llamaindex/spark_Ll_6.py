from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader

import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.end =time.time()
        self.interval = self.end - self.start
        print(f"耗时{self.interval*1000}ms")

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
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


from llama_index.llms.dashscope import DashScope
Settings.llm = DashScope( # 指定TitleExtractor()的标题生成模型
    model_name="qwen-plus",
    api_key=os.getenv("ALI_API_KEY"),
)

new_pipeline = IngestionPipeline( #按顺序处理文档
    transformations=[
        #把长文档切分成小块 每块300token 相邻重叠100token
        SentenceSplitter(chunk_size=300,chunk_overlap=100),
        TitleExtractor(),
        #为每个Node生成向量 的模型
        Settings.embed_model,
    ],
)


from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader

documents = SimpleDirectoryReader(
    "./data",
    required_exts=[".pdf"],
    file_extractor={".pdf":PyMuPDFReader()},

).load_data() #返回Document列表
#加载缓存
new_pipeline.load("./pipeline_storage")
with Timer():
    nodes = new_pipeline.run(documents=documents)

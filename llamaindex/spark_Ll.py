from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader
# 加载本地数据  pdf 加载器还有SmartPDFLoader LlamaParse
reader = SimpleDirectoryReader(
    input_dir="./data",          # 目标目录
    recursive=False,             # 是否递归遍历子目录
    required_exts=[".pdf"],      # (可选) 只读取指定后缀的文件
    file_extractor={".pdf":PyMuPDFReader()} #指定加载器

)
documents = reader.load_data()
if __name__=="__main__":
    print(len(documents))
    print(documents[1].text)
    print("$"*24)
    print(documents)



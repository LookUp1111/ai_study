from llama_index.readers.feishu_docs import FeishuDocsReader

app_id = ""
app_secret = ""
#https://my.feishu.cn/docx/KC1QdmyFLoycKsxaSVlcjX32n6f
doc_ids = [""]
#定位飞书文档加载器
loader = FeishuDocsReader(app_id,app_secret)
#加载文档
documents = loader.load_data(document_ids = doc_ids)

#显示前100个字符
print(documents[0].text[:1000])

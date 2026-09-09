import re
#按照sentence 来切分
text = "RAG 全称检索增强生成，是大模型落地最主流的技术方案。传统大模型依靠训练数据回答问题，存在知识滞后、容易编造幻觉、私有数据无法读取的缺陷。RAG 把外部知识库和大模型结合：先对用户问题做向量检索，从文档库中匹配相关资料片段，再把检索到的真实上下文连同问题一起送入大模型，让模型基于参考素材生成答案。它无需重新训练大模型，更新资料只需要替换知识库，成本更低、可控性更强。广泛应用于智能客服、企业文档问答、知识库助手。但检索质量直接决定回答效果，存在召回不准、上下文冗余等痛点，需要优化向量库、重排和提示词策略。"
#正则表达匹配中文的结束标点符号
sentences = re.split(r'(。|？|！|……|\.\.\.)',text)
#重新组合句子和结尾的标点符号
chunks = [
    sentence + (punctuation if punctuation else '')
    for sentence,punctuation in zip(sentences[::2],sentences[1::2]) #zip(a,b)：把两个列表按顺序配对打包：奇数会放弃最后一个
         ]
# 如果列表长度是奇数，说明最后还有一段无标点文本，手动补上
if len(sentences)%2 == 1 and sentences[-1].strip():
    chunks.append(sentences[-1])
#重新组合句子和结尾的标点符号
for i,chunk in enumerate(chunks):
    print(f"块{i+1}：{len(chunk)}:{chunk}")

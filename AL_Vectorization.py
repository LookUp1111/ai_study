import os
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
load_dotenv()

client = OpenAI(
    api_key=os.getenv("ALI_API_KEY"),
    base_url="https://ws-c527z7l6jv0lp8w1.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
def get_embedding(text):
    resp = client.embeddings.create(
        model="text-embedding-v1",
        input=text,
        dimensions=256  # 向量维度
    )
    return resp.data[0].embedding


def cosine_similarty(A,B):
    dot_product = np.dot(A,B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    return dot_product / (norm_A * norm_B)

A = get_embedding("你好，老王爱吃瓜")
B = get_embedding("老王爱吃什么")
C = get_embedding("老王不爱吃瓜")
D = get_embedding("瓜爱吃老王")

print(cosine_similarty(A,D))

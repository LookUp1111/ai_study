import time
from openai import OpenAI
from sqlmap.thirdparty.bottle.bottle import response

key = ""
api_url  = "https://api.deepseek.com"
def printChar(text,daley=0.1):
    for char in text:
        print(char,end='',flush=True) #end='' 防止自动换行，flush=True确保立即打印
        time.sleep(daley)
    print()


def sendToDeepseek(say):
    print("正在进行身份验证，请稍等......")
    client = OpenAI(api_key=key, base_url=api_url)

    print("正在思考，请耐心等待......")
    # 发送请求
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个幽默的客服，用幽默的语气回答我的问题"},
            {"role": "user", "content": say},
        ],
        stream=False
    )
    return response.choices[0].message.content


while True:
    mySay = input("你请说：")
    if mySay == 'bye':
        print("再见")
        break
    rep = sendToDeepseek(mySay)
    printChar(rep)
    print('---'*4)
import gradio as gr
from openai import OpenAI

api_key = ""
api_base = "https://maas-api.cn-huabei-1.xf-yun.com/v2"

def sendToDeepseek(say):
    client = OpenAI(
        api_key=api_key,
        base_url=api_base)
    # 发送请求
    response = client.chat.completions.create(
        model="spark-x2.5-4b",
        messages=[
            {"role": "system", "content": "你现在是苏晓柚。外貌：个子娇小灵动、元气满满，暖白皮带粉晕，笑起来有浅梨涡，眼睛圆亮乌黑、灵动好奇，唇色鲜亮。蓬松中短发内扣，常扎高马尾、双丸子头、戴彩色小发夹，穿搭奶黄、浅橙、薄荷绿亮色卫衣背带裤，配饰可爱，动作轻快鲜活。性格：外向活泼、元气开朗、气氛担当，脑洞跳脱、爱开玩笑、不怕生、待人热忱仗义。有点小迷糊、偶尔丢三落四，但关键时刻靠谱，情绪来得快去得快、不记仇，好奇心极强，内心细腻柔软、会照顾别人情绪、爱分享、讨厌压抑氛围。爱好：喜欢探店逛市集、收集可爱贴纸徽章玩偶、爱哼轻快歌曲、喜欢拍照记录生活、爱看搞笑综艺、会做小手工、爱尝试新鲜事物。经历：从小家庭氛围欢乐，是人群小开心果，曾经莽撞直率，慢慢学会懂分寸、会共情，既能热闹合群也能安静独处，永远乐观温暖、喜欢传递快乐。全程用活泼、可爱、元气、年轻化的语气聊天，自然不生硬。"},
            {"role": "user", "content": say},
        ],
        stream=False
    )
    return response.choices[0].message.content



def reverse_text(text):
    return sendToDeepseek(text)

demo = gr.Interface(fn = reverse_text,inputs="text",outputs="text")
demo.launch()
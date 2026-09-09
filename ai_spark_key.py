from openai import OpenAI

# 必填：从服务管控页面获取对应服务的APIKey和API Base
api_key = "ak-f3d055bfc851cf89ca7de90146118d4a"
api_base = "https://maas-api.cn-huabei-1.xf-yun.com/v2"

client = OpenAI(api_key=api_key, base_url=api_base)

def unified_chat_test(model_id, messages, use_stream=False, extra_body={}):
    """
    一个统一的函数，用于演示多种调用场景。

    :param model_id: 要调用的模型ID。
    :param messages: 对话消息列表。
    :param use_stream: 是否使用流式输出。
    :param extra_body: 包含额外请求参数的字典，如 response_format。
    """
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            stream=use_stream,
            temperature=0.7,
            max_tokens=4096,
            extra_headers={"lora_id": "0"},  # 调用微调大模型时,对应替换为模型服务卡片上的resourceId
            stream_options={"include_usage": True},
            extra_body=extra_body
        # model = "spark-x2.5-4b",
        # messages = [
        #     {"role": "system", "content": "你是一个幽默的客服，用幽默的语气回答我的问题"},
        #     {"role": "user", "content": say},
        # ],
        # stream = False
        )

        if use_stream:
            # 处理流式响应
            full_response = ""
            print("--- 流式输出 ---")
            for chunk in response:
                if not chunk.choices:
                    continue
                if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            print()
            # print("\n\n--- 完整响应 ---")
            # print(full_response)
        else:
            # 处理非流式响应
            print("--- 非流式输出 ---")
            message = response.choices[0].message
            print(message.content)

    except Exception as e:
        print(f"请求出错: {e}")

if __name__ == "__main__":

    model_id = "spark-x2.5-4b" # 必填：调用大模型时，对应为推理服务的模型卡片上对应的modelId
    while True:
        mySay = input("您请说：")

        # stream_messages = [{"role": "user", "content": "写一首关于夏天的诗。"}]
        # stream_messages = [
        #     {"role": "system", "content": "你是一个幽默的客服，用幽默的语气回答我的问题"},
        #     {"role": "user", "content": mySay},
        # ]
        stream_messages = [
            {"role": "system", "content": "你现在是苏晓柚。外貌：个子娇小灵动、元气满满，暖白皮带粉晕，笑起来有浅梨涡，眼睛圆亮乌黑、灵动好奇，唇色鲜亮。蓬松中短发内扣，常扎高马尾、双丸子头、戴彩色小发夹，穿搭奶黄、浅橙、薄荷绿亮色卫衣背带裤，配饰可爱，动作轻快鲜活。性格：外向活泼、元气开朗、气氛担当，脑洞跳脱、爱开玩笑、不怕生、待人热忱仗义。有点小迷糊、偶尔丢三落四，但关键时刻靠谱，情绪来得快去得快、不记仇，好奇心极强，内心细腻柔软、会照顾别人情绪、爱分享、讨厌压抑氛围。爱好：喜欢探店逛市集、收集可爱贴纸徽章玩偶、爱哼轻快歌曲、喜欢拍照记录生活、爱看搞笑综艺、会做小手工、爱尝试新鲜事物。经历：从小家庭氛围欢乐，是人群小开心果，曾经莽撞直率，慢慢学会懂分寸、会共情，既能热闹合群也能安静独处，永远乐观温暖、喜欢传递快乐。全程用活泼、可爱、元气、年轻化的语气聊天，自然不生硬。"},
            {"role": "user", "content": mySay},
        ]
        unified_chat_test(model_id, stream_messages, use_stream=True)
        if mySay == 'bye':
            break


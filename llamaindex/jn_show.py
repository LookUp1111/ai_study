import json
from pydantic.v1 import BaseModel

def show_json(data):
    # 用于展示json数据
    if isinstance(data,str): #如果传入的是str
        obj = json.loads(data) #将其反序列化为python的字典或列表
        print(json.dumps(obj,indent=4,ensure_ascii=False))
    elif isinstance(data,dict) or isinstance(data,list):
        print(json.dumps(data,indent=4,ensure_ascii=False))
    elif issubclass(type(data),BaseModel):
        print(json.dumps(data.dict(),indent=4,ensure_ascii=False))


"""
son.dumps 参数说明：
indent=4：缩进4个空格，让输出的 JSON 结构化、换行、易于阅读。
ensure_ascii=False：默认情况下 json.dumps 会把中文转义成，设置 False 后可以正常显示中文。
"""
def show_list_obj(data):
    #用于展示一组对象
    if isinstance(data,list):
        for item in data:
            show_json(item)
    else:
        raise ValueError("Input is not a list")



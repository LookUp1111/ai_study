import json
import requests
response = requests.post(
    url="http://localhost:9999/joke/invoke",
    #url="http://localhost:9999/joke/playground/",
    json={'input':{'topic':'小明'}}

)
print(json.dumps(response.json(),indent=2,ensure_ascii=False))
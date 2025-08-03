import openai
import os

def test_api():
    os.environ["http_proxy"] = "http://"
    os.environ["https_proxy"] = "http://"
    client = openai.OpenAI(
        api_key="api_key")
    try:
        response = client.models.list()
        print("OpenAI API 连接成功！")
        print('*'*60)
    except Exception as e:
        print("连接失败：", e)
    models = client.models.list()
    print('该 api_key 可用模型如下:')
    for m in models.data:
        print(m.id)

def Request():
    import requests
    url = "https://api.poixe.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": "api_key"}
    data = {
        "model": "claude-3-5-haiku-20241022:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(response.json()["choices"][0]["message"]["content"])
    else:
        print(f"Error: {response.status_code}, {response.text}")

def CDK():
    from openai import OpenAI
    client = OpenAI(api_key="api_key", base_url="https://api.poixe.com/v1")
    completion = client.chat.completions.create(
        model="claude-3-5-haiku-20241022:free",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
    )
    print(completion.choices[0].message.content)

def test_api_cdk():
    os.environ["http_proxy"] = "http://"
    os.environ["https_proxy"] = "http://"
    from openai import OpenAI
    client = OpenAI(api_key="api_key", base_url="https://api.poixe.com/v1")
    try:
        response = client.models.list()
        print("OpenAI API 连接成功！")
        print('*'*60)
    except Exception as e:
        print("连接失败：", e)
    models = client.models.list()
    print('该 api_key 可用模型如下:')
    for m in models.data:
        print(m.id)



if __name__ == '__main__':
    # test_api()
    # which_model()
    # Request()
    # CDK()
    test_api_cdk()

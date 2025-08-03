import openai
import os

def test_api():
    os.environ["http_proxy"] = "http://127.0.0.1:10809"
    os.environ["https_proxy"] = "http://127.0.0.1:10809"
    client = openai.OpenAI(
        api_key="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")
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
    headers = {"Content-Type": "application/json", "Authorization": "sk-WRFlV3D27txa663eVfhBYpYp5fUmJW5zfMara43a8Qjf23mi"}
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
    client = OpenAI(api_key="sk-WRFlV3D27txa663eVfhBYpYp5fUmJW5zfMara43a8Qjf23mi", base_url="https://api.poixe.com/v1")
    completion = client.chat.completions.create(
        model="claude-3-5-haiku-20241022:free",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
    )
    print(completion.choices[0].message.content)

def test_api_cdk():
    os.environ["http_proxy"] = "http://127.0.0.1:10809"
    os.environ["https_proxy"] = "http://127.0.0.1:10809"
    from openai import OpenAI
    client = OpenAI(api_key="sk-WRFlV3D27txa663eVfhBYpYp5fUmJW5zfMara43a8Qjf23mi", base_url="https://api.poixe.com/v1")
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

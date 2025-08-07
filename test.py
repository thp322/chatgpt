import openai
import os

def test_api():
    # 从环境变量获取API密钥
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("请设置OPENAI_API_KEY环境变量")
        return
    
    os.environ["http_proxy"] = "http://127.0.0.1:10809"
    os.environ["https_proxy"] = "http://127.0.0.1:10809"
    client = openai.OpenAI(api_key=api_key)
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
    # 从环境变量获取API密钥
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("请设置OPENAI_API_KEY环境变量")
        return
    
    base_url = os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    url = f"{base_url}/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {
        "model": "gpt-4",
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
    # 从环境变量获取API密钥
    api_key = os.environ.get('OPENAI_API_KEY')
    base_url = os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    
    if not api_key:
        print("请设置OPENAI_API_KEY环境变量")
        return
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    completion = client.chat.completions.create(
        model="gpt-4",
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
    
    # 从环境变量获取API密钥
    api_key = os.environ.get('OPENAI_API_KEY')
    base_url = os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    
    if not api_key:
        print("请设置OPENAI_API_KEY环境变量")
        return
    
    client = OpenAI(api_key=api_key, base_url=base_url)
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

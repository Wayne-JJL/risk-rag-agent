import os
from dotenv import load_dotenv
from openai import OpenAI
"""
负责初始化模型客户端和统一调用
"""

load_dotenv()

def get_client():
    return OpenAI(
        api_key=os.getenv("API_KEY") or os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("BASE_URL", "https://api.deepseek.com")
    )
def chat_completion(messages, model="deepseek-chat", temperature=0.3):
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    content = response.choices[0].message.content
    usage = getattr(response, "usage", None)

    return {
        "content": content,
        "usage": usage
    }
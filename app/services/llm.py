from app.config import OLLAMA_CHAT_URL
import ollama
import requests
import json


def get_ai_response(messages:list[dict]):
    print("++++",messages,"+++++++")
    response = requests.post(OLLAMA_CHAT_URL,json={
        "model":"llama3.2:3b",
        "messages":messages,
        "stream":True
    },
    stream=True
    )
    # response_data = response.json()
    # return response_data["message"]["content"]
    # yield response_data["message"]["content"]
    for chunk in response.iter_lines():
        # yield chunk
        ollama_response = json.loads(chunk)
        if "message" in ollama_response:
            yield ollama_response["message"]["content"]
    

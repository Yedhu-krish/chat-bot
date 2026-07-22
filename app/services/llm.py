from app.config import OPENAI_API_KEY,OLLAMA_URL
import ollama
import requests
import json

# def get_ai_response(message:str):
#     response = requests.post(OLLAMA_URL,json={
#         "model":"llama3.2:3b",
#         "messages":[
#             {
#                 "role":"user",
#                 "content":message
#             }
#         ],
#         "stream":False
#     })
#     response_data=response.json()
#     # response = ollama.chat(model="llama3.2:3b",messages=[
#     #     {
#     #     "role":"user",
#     #     "content":message
#     #     }
#     # ])
#     return response_data["message"]["content"]

def get_ai_response(messages:list[dict]):
    response = requests.post(OLLAMA_URL,json={
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
    

import ollama

from app.config import EMBEDDING_MODEL,OLLAMA_HOST

client = ollama.Client(host=OLLAMA_HOST)


def generate_embedding(chunk:str) -> list[float]:
    response = client.embed(
        model=EMBEDDING_MODEL,
        input=chunk
    )

    return response.embeddings[0]
import ollama
from app.config import EMBEDDING_MODEL

def generate_embedding(chunk:str) -> list[float]:
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=chunk
    )

    return response.embeddings[0]
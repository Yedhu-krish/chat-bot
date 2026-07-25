from app.services.document_service.embedding_service import generate_embedding
from app.database.models import DocumentChunk
from sqlalchemy import select

def search_similar_chunks(db,query_embedding:list[float],document_id:int,limit:int=5) -> list[DocumentChunk]:
    stmnt = select(DocumentChunk).where(DocumentChunk.document_id == document_id).order_by(DocumentChunk.embedding.cosine_distance(query_embedding)).limit(limit)
    results = db.execute(stmnt)
    return results.scalars().all()

def build_rag_prompt(question:str,chunks:list[str]):

    context = "\n\n".join(chunk.content for chunk in chunks)

    return [
        {
            "role":"user",
            "content":f"""
            Answer the question using the context below.

            Context:
            {context}

            Question:
            {question}
            """
        }
    ]


def question_handling(db,question:str,document_id:int):
    query_embedding = generate_embedding(chunk=question)
    limit = 5
    chunks = search_similar_chunks(db,query_embedding=query_embedding,document_id=document_id,limit=limit)
    return build_rag_prompt(question=question,chunks=chunks)
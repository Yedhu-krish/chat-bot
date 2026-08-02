from sqlalchemy import select

from app.database.models import DocumentChunk
from app.services.document_service.embedding_service import generate_embedding
from app.services.document_service.document_service import get_document_ids_from_conversation


def search_similar_chunks(db,query_embedding:list[float],document_ids:list[int],limit:int=5) -> list[DocumentChunk]:
    if not document_ids:
        return []
    stmnt = select(DocumentChunk).where(DocumentChunk.document_id.in_(document_ids)).order_by(DocumentChunk.embedding.cosine_distance(query_embedding)).limit(limit)
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


def question_handling(db,question:str,conversation_id:int):
    query_embedding = generate_embedding(chunk=question)
    limit = 5
    document_ids = get_document_ids_from_conversation(db=db,conversation_id=conversation_id)
    chunks = search_similar_chunks(db,query_embedding=query_embedding,document_ids=document_ids,limit=limit)
    return build_rag_prompt(question=question,chunks=chunks)
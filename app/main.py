from fastapi import FastAPI
from app.routes import chat,auth,doc
from app.database import models
from app.database.database import Base,engine

app = FastAPI()

app.include_router(chat.router)
app.include_router(auth.auth_router)
app.include_router(doc.doc_router)


Base.metadata.create_all(bind=engine)
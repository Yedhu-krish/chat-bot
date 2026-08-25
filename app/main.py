from fastapi import FastAPI
from app.routes import chat,auth,doc
# from app.database import models
# from app.database.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(chat.router)
app.include_router(auth.auth_router)
app.include_router(doc.doc_router)


# Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://chat-bot.yedhuk0001.workers.dev"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
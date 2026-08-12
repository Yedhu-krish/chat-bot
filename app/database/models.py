from app.database.database import Base
from sqlalchemy import Column,String,Text,Integer,ForeignKey,DateTime,func,Boolean,text,BigInteger
from datetime import datetime,timezone
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy import Enum as SQLEnum
from app.database.enums import DocumentStatus

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    username = Column(String(100),nullable=False,unique=True)
    email = Column(String(255),unique=True,nullable=True)
    hashed_password = Column(String(255),nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean,nullable=False,server_default=text("true"))
    conversations = relationship("Conversation",back_populates="user")
    refresh_tokens = relationship("RefreshToken",back_populates="user")
    documents = relationship("Document",back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer,primary_key=True)
    title = Column(String(length=255))
    user_id = Column(Integer,ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    user = relationship("User",back_populates="conversations")
    messages = relationship("Message",back_populates="conversation",cascade="all, delete-orphan")
    documents = relationship("ConversationDocument",back_populates="conversation",cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer,primary_key=True)
    role = Column(String)
    content = Column(Text)
    conversation_id = Column(Integer,ForeignKey("conversations.id"))
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
    conversation = relationship("Conversation",back_populates="messages")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer,primary_key=True)
    token = Column(String,nullable=False,unique=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    revoked = Column(Boolean,nullable=False,server_default=text("false"))
    expires_at = Column(DateTime(timezone=True),nullable=False)
    user = relationship("User",back_populates="refresh_tokens")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer,primary_key=True)
    filename = Column(String(length=255),nullable=False)
    s3_key = Column(String(length=512),nullable=False)
    file_type = Column(String(length=100),nullable=False)
    file_size = Column(BigInteger,nullable=False)
    uploaded_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    status = Column(SQLEnum(DocumentStatus),default=DocumentStatus.PROCESSING)
    error_message = Column(Text, nullable=True)
    user = relationship("User",back_populates="documents")
    chunks = relationship("DocumentChunk",back_populates="document",cascade="all, delete-orphan")
    conversations = relationship("ConversationDocument",back_populates="document",cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer,primary_key=True)
    document_id = Column(Integer,ForeignKey("documents.id"),nullable=False)
    content = Column(Text,nullable=False)
    chunk_number = Column(Integer,)
    embedding = Column(Vector(768))
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    document = relationship("Document",back_populates="chunks")

class ConversationDocument(Base):
    __tablename__ = "conversation_documents"

    id = Column(Integer,primary_key=True)
    conversation_id = Column(Integer,ForeignKey("conversations.id"))
    document_id = Column(Integer,ForeignKey("documents.id"))
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    conversation = relationship("Conversation",back_populates="documents")
    document = relationship("Document",back_populates="conversations")

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pgvector.sqlalchemy import Vector 

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False) 
    bot_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ChatbotData(Base):
    __tablename__ = "chatbot_data"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    embedding_vector = Column(Vector(1024))  # Gunakan tipe data Vector dari pgvector
    additional_info = Column(JSONB, default={}, server_default='{}')  
    timestamp = Column(DateTime, default=datetime.utcnow)
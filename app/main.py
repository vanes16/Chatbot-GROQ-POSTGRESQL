from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import init_db, get_db
from app.core.chatbot import get_chatbot_response
from app.models.db_models import ChatHistory, ChatbotData 
from app.models.embedding_models import EmbeddingModel 
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel

# Pydantic Models
class DomainChatRequest(BaseModel):
    user_input: str

class DomainChatResponse(BaseModel):
    response: str
    status: str = "success"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

# Initialize FastAPI
app = FastAPI(lifespan=lifespan)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://react-chat-one-livid.vercel.app",
        "https://7c08-114-4-213-10.ngrok-free.app ",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "API is running successfully!"}

# Chat Endpoint
@app.post("/chat")
async def chat(user_input: str, db: AsyncSession = Depends(get_db)):
    try:
        normalized_input = user_input.lower().strip(" ?!.,") 
        response = await get_chatbot_response(
            user_input=normalized_input,
            db_session=db  
        )

        chat_history = ChatHistory(user_input=user_input, bot_response=response)
        db.add(chat_history)
        await db.commit()
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")

# Domain Chat Endpoint
@app.post("/api/domain-chat", response_model=DomainChatResponse)
async def domain_chat(
    request_data: DomainChatRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        
        normalized_input = request_data.user_input.lower().strip(" ?!.,")
        response = await get_chatbot_response(
            user_input=normalized_input,
            db_session=db
        )

        chat_history = ChatHistory(
            user_input=request_data.user_input,
            bot_response=response,
        )
        db.add(chat_history)
        await db.commit()
        
        return DomainChatResponse(
            response=response,
            status="success"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan: {str(e)}"
        )


# Add Chatbot Data Endpoint
@app.post("/add-chatbot-data")
async def add_chatbot_data(
    question: str,
    answer: str,
    additional_info: Optional[Dict] = None, 
    db: AsyncSession = Depends(get_db)
):
    try:
        embedding_model = EmbeddingModel()
        normalized_input = question.lower().strip(" ?!.,") 
        embedding_vector = embedding_model.get_embedding(normalized_input)
        
        if additional_info is None:
            additional_info = {}
        
        chatbot_data = ChatbotData(
            question=normalized_input,
            answer=answer,
            embedding_vector=embedding_vector,  
            additional_info=additional_info, 
            timestamp=datetime.utcnow()  
        )
        
        db.add(chatbot_data)
        await db.commit()
        
        return {"message": "Data berhasil ditambahkan!", "id": chatbot_data.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from brain.agent import jarvis_brain
from loguru import logger

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received message from {request.user_id}: {request.message}")
    response_text = await jarvis_brain.get_response(request.user_id, request.message)
    return ChatResponse(response=response_text)

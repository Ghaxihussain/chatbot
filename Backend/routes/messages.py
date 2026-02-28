from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.routing import JSONResponse
from sqlalchemy import insert, select
from ..chatbot import model, get_response
from langchain_core.messages import SystemMessage, HumanMessage
from ..config.database import Chat, User, async_session, Message
from .users import get_current_user



router = APIRouter(prefix = "/chat")


@router.post('/')
async def send_message(message, chat_id, current_user: User = Depends(get_current_user)):
    res = await get_response(message, int(chat_id), user_id= current_user.id)
    return JSONResponse(content = res, status_code = status.HTTP_200_OK)



@router.get('/{chat_id}')
async def get_msgs(chat_id: int, current_user: User = Depends(get_current_user)):
    
    async with async_session() as session:
        chat = await session.execute(select(Message).where(Message.user_id == current_user.id, Message.chat_id == chat_id))
        chat = chat.scalars().all()
        if not chat:
            raise HTTPException(detail = "Chat does not exists", status_code = status.HTTP_404_NOT_FOUND)
    
    res = [{"content" : msg.content, "role": msg.role} for msg in chat]

    return JSONResponse(content = res, status_code= status.HTTP_200_OK)
from fastapi import APIRouter, Depends
from fastapi.routing import JSONResponse
from sqlalchemy import JSON, insert, select
from ..chatbot import model
from langchain_core.messages import SystemMessage, HumanMessage
from ..config.database import Chat, async_session, Message, User
from .users import get_current_user





router = APIRouter(prefix="/chat")



@router.post('/create')
async def create_chat(message:str, current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    title_chat = [SystemMessage(content = "Create a one sutable title for this message, no bold, simple text"), HumanMessage(content = message)]
    title = model.invoke(title_chat)
    async with async_session() as session:
        await session.execute(insert(Chat).values(title = title.content, user_id = int(user_id)))
        await session.commit()
    return JSONResponse(content = f"{title.content} created")





@router.get('/conversation/history')
async def get_convo(current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    async with async_session() as session:
        chats = await session.execute(select(Chat).where(Chat.user_id == int(user_id)))

    chats = chats.scalars().all()
    res = [
        {"title": chat.title} for chat in chats
    ] 
    return JSONResponse(content = res)





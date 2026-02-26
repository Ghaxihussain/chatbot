from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy import insert, select
from .config.database import User, Message, Chat, async_session
import asyncio
load_dotenv()

model = ChatOpenAI(model = "gpt-4o-mini", temperature = 1)



chat_templete = ChatPromptTemplate([
    ("system", "You are a chatbot"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")]
)


async def get_history(chat_id: int):
    async with async_session() as session:
        result = await session.execute(select(Message).where(Message.chat_id == chat_id))
    
    result = result.scalars().all()
    

    res = []


    for rows in result:
        if rows.role == "user": res.append(HumanMessage(content = rows.content))
        else: res.append(AIMessage(content = rows.content))
    


    return res



async def get_response(message: str, chat_id: int, user_id: int):
    history = await get_history(chat_id)
    
    chat_templete = ChatPromptTemplate([
            ("system", "You are a chatbot"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")])
    

    chain = chat_templete | model
    res = await chain.ainvoke({
            "chat_history": history,
            "input": message
        })
    async with async_session() as session:
        await session.execute(insert(Message).values(content = message, chat_id = chat_id, role = "user", user_id = user_id))
        await session.execute(insert(Message).values(content = res.content, chat_id = chat_id, role = "ai", user_id = user_id))
        await session.commit()

    return res.content
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy import insert, select
from config.database import User, Message, Chat, async_session, init_db
import asyncio
load_dotenv()

model = ChatOpenAI(model = "gpt-4o-mini", temperature = 1)



chat_templete = ChatPromptTemplate([
    ("system", "You are a chatbot"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")]
)



async def main():
    await init_db()
    async with async_session() as session:
        result = await session.execute(insert(User).values(username="ghazihussainn", name="ghazi", password="jwj").returning(User.id))
        user_id = result.scalar_one()
        await session.execute(insert(Chat).values(title="First chat", user_id=user_id))
        await session.execute(insert(Message).values(content = "Hey!", chat_id = 1, role = "user"))
        await session.commit()

        chat_history = []
        ## probably the chat id would be 1, when running first time, so i have to find all the msgs sotrted with dattime for the chathistory

        chat_his = await session.execute(select(Message.role, Message.content).where(Message.chat_id == 1))
        print(chat_his.all())

    # while True:
    #     user = input("User: ")
    #     chat_templete.invoke({"chat_history": chat_history, "input": user})
    #     chat_history.append(HumanMessage(content = user))
    #     res = model.invoke(chat_history)
    #     chat_history.append(AIMessage(content = res.content))
    #     print("chatbot: ", res.content)



asyncio.run(main())
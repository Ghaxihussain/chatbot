from fastapi import FastAPI
from .routes import messages, chats, users


app = FastAPI()
app.include_router(messages.router)
app.include_router(chats.router)
app.include_router(users.router)








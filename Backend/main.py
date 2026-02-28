from fastapi import FastAPI
from .routes import messages, chats, users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="Frontend/"), name="static")
app.include_router(messages.router)
app.include_router(chats.router)
app.include_router(users.router)








from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from ..config.database import User,async_session
from sqlalchemy import select, insert

router = APIRouter(prefix = "/accounts")




@router.post("/signup")
async def create_user(username: str, password:str, name: str):
    async with async_session() as session:
        query = select(User).where(User.username == username)
        res = await session.execute(query)
        res = res.scalars().all()
        if res :
            raise HTTPException(detail = f"User {username} already exists", status_code = status.HTTP_306_RESERVED)
        await session.execute(insert(User).values(username = username, password = password, name = name))
        await session.commit()


    return JSONResponse(content = f"{username} created")
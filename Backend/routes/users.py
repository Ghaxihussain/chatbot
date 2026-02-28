from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from ..config.database import User,async_session
from sqlalchemy import select, insert
from fastapi.responses import Response
import jwt
from datetime import datetime, timedelta

SECRET = "ghazihussainn"

def create_token(user_id: int, username: str):
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=7) 
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verify_token(token: str):
    print(f"this is the {token}")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return {"username": payload["username"], "user_id": payload["user_id"]}
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")



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


@router.post('/login')
async def login_user(username: str, password: str, response: Response):
    async with async_session() as session:
        res = await session.execute(select(User).where(User.username == username))
        user = res.scalars().first()

        if not user:
            raise HTTPException(detail=f"User {username} does not exist", status_code=status.HTTP_404_NOT_FOUND)

        if password != user.password:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")
    token = create_token(username=username, user_id=user.id)
    
    response.set_cookie(
            key="access_token", 
            value=create_token(username=username, user_id=user.id),
            httponly=True,      
            samesite="lax",
            path="/",           
            max_age=604800      
        )
    return 




async def get_current_user(request: Request, res: Response):
    res.delete_cookie("access_token")
    token = request.cookies.get("access_token")
    uid = verify_token(token)["user_id"]
    print("TOKEN:", token) 
    async with async_session() as db:
        user = await db.execute(select(User).where(User.id == uid))
    user = user.scalar_one_or_none()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "Invalid Cookie")
    return user



@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Logged out"}
from fastapi import APIRouter, status
from app.db import db

from app.schema import schemas


router = APIRouter(tags=["Users"], prefix="/user")



# @router.get("/", response_model=schemas.UserOut, status_code=status.HTTP_200_OK)

@router.get("/")
async def get_current_user(user_id: str):
    user = await db.user.find_unique(where={"id": user_id})
    return user



from fastapi import APIRouter
from app.db import db

router = APIRouter(tags=["Users"], prefix="/user")


@router.get("/")
def get_current_user(user_id: str):
    user = db.user.find_unique(where={"id": user_id})
    return user

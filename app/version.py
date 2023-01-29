
from fastapi import APIRouter
from app.api import user_api

router = APIRouter()

def version_one():
    router.include_router(user_api.router)


version_one()
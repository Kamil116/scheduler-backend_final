
from fastapi import APIRouter
from app.api import userapi
from app.api import groupapi
from app.api import courseapi
from app.api import slotapi

from app.api import seedapi


router = APIRouter()

def version_one():
    router.include_router(userapi.router)
    router.include_router(groupapi.router)
    router.include_router(courseapi.router)
    router.include_router(slotapi.router)

    # router.include_router(seedapi.router)




version_one()
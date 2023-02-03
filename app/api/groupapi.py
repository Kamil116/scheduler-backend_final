from fastapi import APIRouter
from app.db import db


router = APIRouter(tags=["Groups"], prefix="/group")



@router.get("/")
def get_all_groups():
    groups = db.group.find_many()
    return groups


@router.get("/:group_id")
def get_group_by_id(group_id: str):
    group = db.group.find_unique(where={"id": group_id})
    return group


@router.get("/:specific_group")
def get_group_by_specific_group(specific_group: str):
    group = db.group.find_first(where={"specific_group": specific_group})
    return group

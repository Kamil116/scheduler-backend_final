from fastapi import APIRouter
from app.db import db


router = APIRouter(tags=["Courses"], prefix="/course")


@router.get("/")
def get_all_courses():
    courses = db.course.find_many(order={"description": "asc"})
    return courses

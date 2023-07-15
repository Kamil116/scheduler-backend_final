from pydantic import BaseModel


class UpdateCourse(BaseModel):
    title: str
    start: str
    end: str
    extendedProps = {'id': 0, 'room': '', 'course': '', 'group': '', 'instructorName': ''}


class NewCourse(BaseModel):
    title: str
    start: str
    end: str
    extendedProps = {'room': '', 'course': '', 'group': '', 'instructorName': ''}

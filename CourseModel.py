from pydantic import BaseModel


class Course(BaseModel):
    title: str
    start: str
    end: str
    extendedProps = {'id': 0, 'room': '', 'course': '', 'group': '', 'instructorName': ''}

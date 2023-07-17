from fastapi import FastAPI

from CourseModel import UpdateCourse, NewCourse
from parsedDataToDatabase import coursesDatabase
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/get/')
async def get_all_courses():
    return all_courses()


@app.delete('/delete/{course_id}')
async def delete_course(course_id):
    coursesDatabase.delete_course(course_id)

    return all_courses()


@app.put('/update')
async def update_course(course_to_update: UpdateCourse):
    answer = coursesDatabase.get_courses()

    if len(answer) == 0:
        return {'Message': 'We have no courses in database'}

    coursesDatabase.update_course_with_id(course_to_update.title,
                                          course_to_update.start,
                                          course_to_update.end,
                                          course_to_update.extendedProps['id'],
                                          course_to_update.extendedProps['room'],
                                          course_to_update.extendedProps['course'],
                                          course_to_update.extendedProps['group'],
                                          course_to_update.extendedProps['instructorName']
                                          )

    return all_courses()


@app.post('/create')
async def create_course(course_to_create: NewCourse):
    coursesDatabase.add_course(course_to_create.title,
                               course_to_create.start,
                               course_to_create.end,
                               course_to_create.extendedProps['room'],
                               course_to_create.extendedProps['course'],
                               course_to_create.extendedProps['group'],
                               course_to_create.extendedProps['instructorName']
                               )

    return all_courses()


def all_courses():
    answer = coursesDatabase.get_courses()

    if len(answer) == 0:
        return {'Message': 'We have no courses in database'}

    result = []
    for course in answer:
        if course[6] != 'None':
            result.append({'title': course[1], 'start': course[2], 'end': course[3],
                           'extendedProps': {'id': course[0], 'room': course[4], 'course': course[5],
                                             'group': course[6],
                                             'instructorName': course[7]}})
        else:
            result.append({'title': course[1], 'start': course[2], 'end': course[3],
                           'extendedProps': {'id': course[0], 'room': course[4], 'course': course[5],
                                             'instructorName': course[7]}})
    return result

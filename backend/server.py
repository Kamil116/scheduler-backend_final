from fastapi import FastAPI

from backend.CourseModel import Course
from parsedDataToDatabase import coursesDatabase
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def root():
    return {'Example': 'This is an example', 'data': 0}


@app.get('/get/')
async def get_all_courses():
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


@app.delete('/delete/{course_id}')
async def delete_course(course_id):
    coursesDatabase.delete_course(course_id)

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


@app.put('/update')
async def update_course(course_to_update: Course):
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

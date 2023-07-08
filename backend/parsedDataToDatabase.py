import json
import db

coursesDatabase = db.CoursesInfoDatabase('courses.db')

json_file = 'output.json'
cube = '1'

with open(json_file) as json_data:
    data = json.load(json_data)

for course in data:
    # Incorrect info in json file about elective courses on p. e.
    if course['extendedProps']['instructorName'] == 'Elective courses on Physical Education':
        coursesDatabase.add_course(course['extendedProps']['instructorName'],
                                   course['start'], 'sport center', course['extendedProps']['course'], '')
    else:
        coursesDatabase.add_course(course['title'], course['start'], course['extendedProps']['room'],
                                   course['extendedProps']['course'],
                                   course['extendedProps']['instructorName'])

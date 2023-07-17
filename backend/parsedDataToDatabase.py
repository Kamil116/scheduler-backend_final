from backend import db
import json

coursesDatabase = db.CoursesInfoDatabase("data/courses.db")
# coursesDatabase = db.CoursesInfoDatabase('test.db')

json_file = "data/output.json"

with open(json_file) as json_data:
    data = json.load(json_data)

if len(coursesDatabase.get_courses()) == 0:
    for course in data:
        try:
            coursesDatabase.add_course(course['title'], course['start'], course['end'], course['extendedProps']['room'],
                                       course['extendedProps']['course'], course['extendedProps']['group'],
                                       course['extendedProps']['instructorName'])
        except KeyError:
            # In case when we do not have info about group. It is lectures and tutorials.
            coursesDatabase.add_course(course['title'], course['start'], course['end'], course['extendedProps']['room'],
                                       course['extendedProps']['course'], "None",
                                       course['extendedProps']['instructorName'])

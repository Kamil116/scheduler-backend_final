import sqlite3


class StudentsInfoDatabase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, course TEXT, st_group TEXT)")
        self.connection.commit()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT 1 FROM profile where user_id == '{key}'".format(key=user_id)).fetchone()
            return result != None

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO profile VALUES(?, ?, ?)", (user_id, '', ''))

    def get_course(self, user_id):
        return self.cursor.execute(
            "SELECT course FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()[0]

    def get_group(self, user_id):
        return self.cursor.execute(
            "SELECT st_group FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()[0]

    def get_users(self):
        return self.cursor.execute(
            "SELECT user_id FROM profile").fetchall()

    def update_course(self, text, user_id):
        self.cursor.execute('''UPDATE profile SET course = ? WHERE user_id = ?''', (text, user_id))
        self.connection.commit()

    def update_group(self, text, user_id):
        self.cursor.execute('''UPDATE profile SET st_group = ? WHERE user_id = ?''', (text, user_id))
        self.connection.commit()


class CoursesInfoDatabase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS courses(id INTEGER PRIMARY KEY, title TEXT,"
            " start_time TEXT, end_time TEXT, room TEXT, target_course TEXT, target_group TEXT, instructor Text)")
        self.connection.commit()

    def add_course(self, title, start, end, room, target_course, target_group, instructor):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO courses(title, start_time, end_time, room, target_course, target_group, instructor)"
                " VALUES(?, ?, ?, ?, ?, ?, ?)",
                (title, start, end, room, target_course, target_group, instructor))

    def get_courses(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM courses").fetchall()

    def update_course_with_id(self, title, start_time, end_time, identifier, room, course, group, instructor_name):
        self.cursor.execute('''UPDATE courses SET title = ? WHERE id = ?''', (title, identifier))
        self.cursor.execute('''UPDATE courses SET start_time = ? WHERE id = ?''', (start_time, identifier))
        self.cursor.execute('''UPDATE courses SET end_time = ? WHERE id = ?''', (end_time, identifier))
        self.cursor.execute('''UPDATE courses SET room = ? WHERE id = ?''', (room, identifier))
        self.cursor.execute('''UPDATE courses SET target_course = ? WHERE id = ?''', (course, identifier))
        self.cursor.execute('''UPDATE courses SET target_group = ? WHERE id = ?''', (group, identifier))
        self.cursor.execute('''UPDATE courses SET instructor = ? WHERE id = ?''', (instructor_name, identifier))
        self.connection.commit()

    def get_course_start_time(self, course_name):
        return self.cursor.execute(
            "SELECT start_time FROM courses WHERE title == '{key}'".format(key=course_name)).fetchall()

    def delete_course(self, course_id):
        return self.cursor.execute(
            "DELETE FROM courses WHERE id == '{key}'".format(key=course_id))

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
            "CREATE TABLE IF NOT EXISTS courses(title TEXT,"
            " start_time TEXT, room TEXT, target_course TEXT, instructor Text)")
        self.connection.commit()

    def add_course(self, title, start, room, target_course, instructor):
        with self.connection:
            return self.cursor.execute("INSERT INTO courses VALUES(?, ?, ?, ?, ?)",
                                       (title, start, room, target_course, instructor))

    def get_courses(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM courses").fetchall()

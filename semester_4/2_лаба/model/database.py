import sqlite3
from model.Student import Student, ProgrammingLanguage


class Database:
    def __init__(self, db_path="students.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    patronymic TEXT NOT NULL,
                    course INTEGER NOT NULL,
                    group_name TEXT NOT NULL,
                    total_works INTEGER NOT NULL,
                    completed_works INTEGER NOT NULL,
                    programming_language TEXT NOT NULL
                )
            """)

    def get_all_students(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM students")
            return [self._row_to_student(row) for row in cursor.fetchall()]

    def _row_to_student(self, row):
        return Student(
            name=row[1],
            surname=row[2],
            patronymic=row[3],
            course=row[4],
            group=row[5],
            total_number_of_works=row[6],
            number_of_completed_tasks=row[7],
            programming_language=ProgrammingLanguage(row[8])
        )
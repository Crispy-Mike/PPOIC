from model.Student import Student,ProgrammingLanguage
import random
from model.helpers import *

class All_Students:
    def __init__(self):
        self.students = []

    def student_search(self, **criteria) -> list:
        massive = []
        for student in self.students:
            if self.matches_all(student, criteria):
                massive.append(student)
        return massive

    def matches_all(self, student, criteria) -> bool:
        for key, value in criteria.items():
            if not self._matches(student, key, value):
                return False
        return True

    def _matches(self, student, key, value):
        if key == 'full_name':
            full = f"{student.surname} {student.name} {student.patronymic}"
            return value.lower() in full.lower()
        elif key == 'group':
            return str(student.group) == str(value)
        elif key == 'course':
            return student.course == value
        elif key == 'programming_language':
            return student.programming_language == value
        elif key == 'total_number_of_works':
            return student.total_number_of_works == value
        elif key == 'number_of_completed_tasks':
            return student.number_of_completed_tasks == value
        elif key == 'uncompleted_works':
            uncompleted = student.total_number_of_works - student.number_of_completed_tasks
            return uncompleted == value
        return False

    def new_student(self, name, surname, patronymic, course, group,
                    total_number_of_works, number_of_completed_tasks, programming_language):
        student = Student(
            name, surname, patronymic, course, group,
            total_number_of_works, number_of_completed_tasks, programming_language
        )
        self.students.append(student)

    def delete_student(self, **criteria) -> list:
        to_delete = []
        for student in self.students:
            if self.matches_all(student, criteria):
                to_delete.append(student)

        for student in to_delete:
            self.students.remove(student)

        return to_delete

    def auto_selection(self):
        print("Генерация студентов...")

        for x in range(50):
            name = random.choice(names)
            surname = random.choice(surnames)
            patronymic = random.choice(patronymics)
            course = random.choice(courses)
            group = random.choice(groups[course])
            total_number_of_works = random.randint(8, 21)
            number_of_completed_tasks = random.randint(0, total_number_of_works)
            programming_language_str = random.choice(programming_languages)

            if programming_language_str == "Python":
                programming_language = ProgrammingLanguage.PYTHON
            elif programming_language_str == "Java":
                programming_language = ProgrammingLanguage.JAVA
            elif programming_language_str == "C++":
                programming_language = ProgrammingLanguage.CPLUSPLUS
            elif programming_language_str == "JavaScript":
                programming_language = ProgrammingLanguage.JAVASCRIPT
            else:
                programming_language = ProgrammingLanguage.PYTHON

            self.new_student(
                name, surname, patronymic, course, group,
                total_number_of_works, number_of_completed_tasks, programming_language
            )

        print(f"Сгенерировано студентов: {len(self.students)}")
        print("Примеры сгенерированных студентов:")
        for i, student in enumerate(self.students[:5]):
            print(f"  {i + 1}. {student}")
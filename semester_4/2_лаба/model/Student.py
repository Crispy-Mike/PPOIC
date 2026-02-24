from dataclasses import dataclass
from enum import Enum


class ProgrammingLanguage(Enum):
    PYTHON = "Python"
    JAVA = "Java"
    CPLUSPLUS = "C++"
    JAVASCRIPT = "JavaScript"


@dataclass()
class Student:
    name:str
    surname:str
    patronymic:str
    course:int
    group:int
    total_number_of_works:int
    number_of_completed_tasks:int
    programming_language:ProgrammingLanguage


    def __post_init__(self):
        if not all([self.name,self.surname,self.patronymic]):
            raise ValueError("ФИО не может быть пустым")
        if not 1<=self.course<=5:
            raise ValueError("Курс не может быть меньше 1 или больше 5")
        if self.total_number_of_works<0:
            raise ValueError("Максимальное количество работ не может быть меньше 0")
        if self.number_of_completed_tasks<0 or self.number_of_completed_tasks>self.total_number_of_works:
            raise ValueError("Выполненная работа не может быть меньше 0 или больше максимального количества работы")

    def to_dict(self)->dict:
        return {
            "name":self.name,
            "surname":self.surname,
            "patronymic":self.patronymic,
            "course":str(self.course),
            "group":str(self.group),
            "total_number_of_works":str(self.total_number_of_works),
            "number_of_completed_tasks":str(self.number_of_completed_tasks),
            "programming_language":self.programming_language.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        return cls(
            name=data['name'],
            surname=data['surname'],
            patronymic=data['patronymic'],
            course=int(data['course']),
            group=data['group'],
            total_number_of_works=int(data['total_number_of_works']),
            number_of_completed_tasks=int(data['number_of_completed_tasks']),
            programming_language=ProgrammingLanguage(data['programming_language'])
        )

    def __str__(self) -> str:
        return (f"{self.name} {self.surname} {self.patronymic} | Курс: {self.course} | Группа: {self.group} | "
                f"Выполнено: {self.number_of_completed_tasks} из {self.total_number_of_works} | {self.programming_language.value}")
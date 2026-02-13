class Student:
    def __init__(self,name:str,surname:str,number_of_group:int):
        self.name=name
        self.surname=surname
        self.number_of_group=number_of_group
        self.exams=[]
        self.materials=[]
        self.marks_of_materials={}
        self.raspisanie={}
        self.classes_per_week=0
        self.attendance = {}  # словарь посещаемости
        self.attendance_history = []  # история изменений посещаемости

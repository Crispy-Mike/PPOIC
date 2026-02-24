# model/xml_handler.py
import xml.sax
import xml.dom.minidom
from model.Student import Student, ProgrammingLanguage


class StudentSAXHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.students = []
        self.current_element = ""
        self.current_student = {}

    def startElement(self, name, attrs):
        self.current_element = name
        if name == "student":
            self.current_student = {}

    def endElement(self, name):
        if name == "student":
            try:
                student = Student.from_dict(self.current_student)
                self.students.append(student)
            except:
                pass
        self.current_element = ""

    def characters(self, content):
        if self.current_element and content.strip():
            self.current_student[self.current_element] = content.strip()


class XMLHandler:
    @staticmethod
    def save_to_xml(students, filename):
        """Сохранение в XML с использованием DOM парсера"""
        doc = xml.dom.minidom.Document()
        root = doc.createElement("students")
        doc.appendChild(root)

        for student in students:
            student_elem = doc.createElement("student")

            # Создаем элементы для каждого поля
            for key, value in student.to_dict().items():
                elem = doc.createElement(key)
                elem.appendChild(doc.createTextNode(str(value)))
                student_elem.appendChild(elem)

            root.appendChild(student_elem)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(doc.toprettyxml(indent="  "))

    @staticmethod
    def load_from_xml(filename):
        """Загрузка из XML с использованием SAX парсера"""
        handler = StudentSAXHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(filename)
        return handler.students
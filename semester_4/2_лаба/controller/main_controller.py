from model.All_Students import All_Students
from model.database import Database
from view.main_window import MainWindow
from view.search_dialog import SearchDialog
from view.delete_dialog import DeleteDialog
from view.add_dialog import AddDialog
from controller.xml_controller import XMLController


class MainController:
    def __init__(self):
        self.model = All_Students()
        self.db = Database()
        self.view = MainWindow(self)
        self.xml_controller = XMLController(self)

        self.current_page = 1
        self.page_size = 10

        self.load_initial_data()

    def show_all(self):
        self.page_size = len(self.model.students)
        self.current_page = 1
        self.refresh_view()
        self.view.page_size_var.set(str(self.page_size))
        print(f"Показаны все записи: {self.page_size} студентов")

    def load_initial_data(self):
        self.model.auto_selection()
        print(f"Загружено студентов: {len(self.model.students)}")
        self.refresh_view()

    def refresh_view(self):
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        page_data = self.model.students[start:end]

        print(f"Всего студентов: {len(self.model.students)}")
        print(f"Отображается страница {self.current_page}, записей: {len(page_data)}")

        self.view.update_table(page_data)

        total_pages = (len(self.model.students) + self.page_size - 1) // self.page_size
        self.view.update_pagination_info(self.current_page, total_pages, len(self.model.students))

    def run(self):
        self.view.window.mainloop()

    def open_search_dialog(self):
        SearchDialog(self.view.window, self)

    def open_delete_dialog(self):
        DeleteDialog(self.view.window, self)

    def open_add_dialog(self):
        AddDialog(self.view.window, self)

    def add_student(self, name, surname, patronymic, course, group,
                    total_works, completed_works, lang):
        from model.Student import ProgrammingLanguage

        lang_map = {
            "Python": ProgrammingLanguage.PYTHON,
            "Java": ProgrammingLanguage.JAVA,
            "C++": ProgrammingLanguage.CPLUSPLUS,
            "JavaScript": ProgrammingLanguage.JAVASCRIPT
        }

        self.model.new_student(
            name, surname, patronymic, course, group,
            total_works, completed_works, lang_map[lang]
        )
        self.refresh_view()

    def build_search_criteria(self, fio, group, course, lang):
        criteria = {}
        if fio.strip():
            criteria['full_name'] = fio.strip()
        if group.strip():
            criteria['group'] = group.strip()
        if course.strip() and course.strip().isdigit():
            criteria['course'] = int(course.strip())
        if lang.strip():
            from model.Student import ProgrammingLanguage
            for prog_lang in ProgrammingLanguage:
                if prog_lang.value == lang:
                    criteria['programming_language'] = prog_lang
                    break
        return criteria

    def build_delete_criteria(self, fio, group, course, lang, total, completed, uncompleted):
        criteria = self.build_search_criteria(fio, group, course, lang)

        if total.strip() and total.strip().isdigit():
            criteria['total_number_of_works'] = int(total.strip())
        if completed.strip() and completed.strip().isdigit():
            criteria['number_of_completed_tasks'] = int(completed.strip())
        if uncompleted.strip() and uncompleted.strip().isdigit():
            criteria['uncompleted_works'] = int(uncompleted.strip())

        return criteria

    def search_students(self, criteria):
        return self.model.student_search(**criteria)

    def delete_students(self, criteria):
        deleted = self.model.delete_student(**criteria)
        self.refresh_view()
        return deleted

    def first_page(self):
        self.current_page = 1
        self.refresh_view()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_view()

    def next_page(self):
        total_pages = (len(self.model.students) + self.page_size - 1) // self.page_size
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_view()

    def last_page(self):
        total_pages = (len(self.model.students) + self.page_size - 1) // self.page_size
        self.current_page = total_pages
        self.refresh_view()

    def change_page_size(self, size):
        self.page_size = size
        self.current_page = 1
        self.refresh_view()

    def save_to_xml(self):
        self.xml_controller.save_to_xml()

    def load_from_xml(self):
        self.xml_controller.load_from_xml()
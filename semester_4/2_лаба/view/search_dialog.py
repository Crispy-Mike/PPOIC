import tkinter as tk
from tkinter import ttk, messagebox
from model.Student import ProgrammingLanguage

class SearchDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Поиск студентов")
        self.dialog.geometry("700x650")
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        self._create_widgets()
        self._center_dialog(parent)

    def _create_widgets(self):
        tk.Label(self.dialog, text="Поиск студентов",
                 font=("Arial", 16, "bold")).pack(pady=20)

        frame = ttk.LabelFrame(self.dialog, text="Условия поиска", padding=20)
        frame.pack(pady=10, padx=30, fill="x")

        ttk.Label(frame, text="ФИО (частичное совпадение):").grid(row=0, column=0, sticky="w", pady=5)
        self.fio_entry = ttk.Entry(frame, width=30)
        self.fio_entry.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Группа:").grid(row=1, column=0, sticky="w", pady=5)
        self.group_entry = ttk.Entry(frame, width=30)
        self.group_entry.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Курс:").grid(row=2, column=0, sticky="w", pady=5)
        self.course_entry = ttk.Entry(frame, width=30)
        self.course_entry.grid(row=2, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Язык программирования:").grid(row=3, column=0, sticky="w", pady=5)
        self.lang_combo = ttk.Combobox(frame, values=["Python", "Java", "C++", "JavaScript"], width=27)
        self.lang_combo.grid(row=3, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Общее число работ:").grid(row=4, column=0, sticky="w", pady=5)
        self.total_entry = ttk.Entry(frame, width=30)
        self.total_entry.grid(row=4, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Выполненных работ:").grid(row=5, column=0, sticky="w", pady=5)
        self.completed_entry = ttk.Entry(frame, width=30)
        self.completed_entry.grid(row=5, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Невыполненных работ:").grid(row=6, column=0, sticky="w", pady=5)
        self.uncompleted_entry = ttk.Entry(frame, width=30)
        self.uncompleted_entry.grid(row=6, column=1, pady=5, padx=10)

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Найти",
                   command=self._on_search, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена",
                   command=self.dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)

        self._create_results_table()

    def _create_results_table(self):
        result_frame = ttk.LabelFrame(self.dialog, text="Результаты поиска", padding=10)
        result_frame.pack(pady=20, padx=30, fill="both", expand=True)

        columns = ('fio', 'course', 'group', 'total', 'completed', 'language')
        self.result_table = ttk.Treeview(result_frame, columns=columns, show='headings', height=10)

        self.result_table.heading('fio', text='ФИО')
        self.result_table.heading('course', text='Курс')
        self.result_table.heading('group', text='Группа')
        self.result_table.heading('total', text='Всего')
        self.result_table.heading('completed', text='Выполнено')
        self.result_table.heading('language', text='Язык')

        self.result_table.column('fio', width=200)
        self.result_table.column('course', width=50)
        self.result_table.column('group', width=70)
        self.result_table.column('total', width=60)
        self.result_table.column('completed', width=70)
        self.result_table.column('language', width=100)

        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_table.yview)
        self.result_table.configure(yscrollcommand=scrollbar.set)

        self.result_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")

    def _on_search(self):
        criteria = self.controller.build_search_criteria(
            self.fio_entry.get(),
            self.group_entry.get(),
            self.course_entry.get(),
            self.lang_combo.get()
        )

        if self.total_entry.get().strip() and self.total_entry.get().strip().isdigit():
            criteria['total_number_of_works'] = int(self.total_entry.get().strip())
        if self.completed_entry.get().strip() and self.completed_entry.get().strip().isdigit():
            criteria['number_of_completed_tasks'] = int(self.completed_entry.get().strip())
        if self.uncompleted_entry.get().strip() and self.uncompleted_entry.get().strip().isdigit():
            criteria['uncompleted_works'] = int(self.uncompleted_entry.get().strip())

        results = self.controller.search_students(criteria)
        self.display_results(results)

        messagebox.showinfo("Результат поиска", f"Найдено студентов: {len(results)}")

    def display_results(self, students):
        for row in self.result_table.get_children():
            self.result_table.delete(row)

        for student in students:
            self.result_table.insert('', tk.END, values=(
                f"{student.surname} {student.name} {student.patronymic}",
                student.course,
                student.group,
                student.total_number_of_works,
                student.number_of_completed_tasks,
                student.programming_language.value
            ))
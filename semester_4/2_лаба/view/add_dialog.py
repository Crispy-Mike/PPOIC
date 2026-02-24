# view/add_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from model.Student import ProgrammingLanguage
from model.helpers import groups, courses


class AddDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавление студента")
        self.dialog.geometry("450x500")
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        self._create_widgets()
        self._center_dialog(parent)

    def _create_widgets(self):
        tk.Label(self.dialog, text="Добавление нового студента",
                 font=("Arial", 16, "bold")).pack(pady=20)

        frame = ttk.LabelFrame(self.dialog, text="Данные студента", padding=20)
        frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Поля ввода
        ttk.Label(frame, text="Фамилия:").grid(row=0, column=0, sticky="w", pady=5)
        self.surname_entry = ttk.Entry(frame, width=30)
        self.surname_entry.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Имя:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Отчество:").grid(row=2, column=0, sticky="w", pady=5)
        self.patronymic_entry = ttk.Entry(frame, width=30)
        self.patronymic_entry.grid(row=2, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Курс:").grid(row=3, column=0, sticky="w", pady=5)
        self.course_combo = ttk.Combobox(frame, values=courses, width=27)
        self.course_combo.grid(row=3, column=1, pady=5, padx=10)
        self.course_combo.bind('<<ComboboxSelected>>', self._update_groups)

        ttk.Label(frame, text="Группа:").grid(row=4, column=0, sticky="w", pady=5)
        self.group_combo = ttk.Combobox(frame, width=27)
        self.group_combo.grid(row=4, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Язык программирования:").grid(row=5, column=0, sticky="w", pady=5)
        self.lang_combo = ttk.Combobox(frame, values=["Python", "Java", "C++", "JavaScript"], width=27)
        self.lang_combo.grid(row=5, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Всего работ:").grid(row=6, column=0, sticky="w", pady=5)
        self.total_entry = ttk.Entry(frame, width=30)
        self.total_entry.grid(row=6, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Выполнено работ:").grid(row=7, column=0, sticky="w", pady=5)
        self.completed_entry = ttk.Entry(frame, width=30)
        self.completed_entry.grid(row=7, column=1, pady=5, padx=10)

        # Кнопки
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Добавить", command=self._on_add, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)

    def _update_groups(self, event):
        course = int(self.course_combo.get())
        self.group_combo['values'] = groups[course]

    def _center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")

    def _on_add(self):
        # Проверка заполнения полей
        if not all([self.surname_entry.get(), self.name_entry.get(),
                    self.patronymic_entry.get(), self.course_combo.get(),
                    self.group_combo.get(), self.lang_combo.get(),
                    self.total_entry.get(), self.completed_entry.get()]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        try:
            self.controller.add_student(
                self.name_entry.get(),
                self.surname_entry.get(),
                self.patronymic_entry.get(),
                int(self.course_combo.get()),
                self.group_combo.get(),
                int(self.total_entry.get()),
                int(self.completed_entry.get()),
                self.lang_combo.get()
            )
            messagebox.showinfo("Успех", "Студент успешно добавлен")
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
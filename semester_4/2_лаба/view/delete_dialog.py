# view/delete_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from model.Student import ProgrammingLanguage


class DeleteDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Удаление студентов")
        self.dialog.geometry("500x450")
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        self._create_widgets()
        self._center_dialog(parent)

    def _create_widgets(self):
        tk.Label(self.dialog, text="Удаление студентов",
                 font=("Arial", 16, "bold")).pack(pady=20)

        frame = ttk.LabelFrame(self.dialog, text="Условия удаления", padding=20)
        frame.pack(pady=20, padx=30, fill="both", expand=True)

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

        # Кнопки
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Удалить", command=self._on_delete, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)

    def _center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")

    def _on_delete(self):
        criteria = self.controller.build_delete_criteria(
            self.fio_entry.get(),
            self.group_entry.get(),
            self.course_entry.get(),
            self.lang_combo.get(),
            self.total_entry.get(),
            self.completed_entry.get(),
            self.uncompleted_entry.get()
        )

        if not criteria:
            messagebox.showerror("Ошибка", "Введите хотя бы одно условие удаления")
            return
        deleted = self.controller.delete_students(criteria)

        if deleted:
            messagebox.showinfo("Удаление", f"Удалено студентов: {len(deleted)}")
            self.dialog.destroy()
        else:
            messagebox.showinfo("Удаление", "Записей для удаления не найдено")
import tkinter as tk
from tkinter import ttk, Menu


class MainWindow:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Лабораторная №2")
        self.window.geometry("1000x800+250+50")

        self._create_menu()
        self._create_toolbar()
        self._create_table()
        self._create_pagination()

    def _create_menu(self):
        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить в XML", command=self.controller.save_to_xml)
        file_menu.add_command(label="Загрузить из XML", command=self.controller.load_from_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.window.quit)

        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Добавить", command=self.controller.open_add_dialog)
        edit_menu.add_command(label="Поиск", command=self.controller.open_search_dialog)
        edit_menu.add_command(label="Удалить", command=self.controller.open_delete_dialog)

    def _create_toolbar(self):
        toolbar = ttk.Frame(self.window)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text="Добавить", command=self.controller.open_add_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Поиск", command=self.controller.open_search_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Удалить", command=self.controller.open_delete_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Сохранить", command=self.controller.save_to_xml).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Загрузить", command=self.controller.load_from_xml).pack(side=tk.LEFT, padx=2)

    def _create_table(self):
        table_frame = ttk.Frame(self.window, relief='sunken', padding=2)
        table_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        columns = ('fio', 'course', 'group', 'total', 'completed', 'language')
        self.table = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        self.table.heading('fio', text='ФИО студента')
        self.table.heading('course', text='Курс')
        self.table.heading('group', text='Группа')
        self.table.heading('total', text='Всего работ')
        self.table.heading('completed', text='Выполнено')
        self.table.heading('language', text='Язык')

        self.table.column('fio', width=280)
        self.table.column('course', width=70)
        self.table.column('group', width=100)
        self.table.column('total', width=80)
        self.table.column('completed', width=80)
        self.table.column('language', width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_pagination(self):
        pagination_frame = ttk.Frame(self.window)
        pagination_frame.pack(fill=tk.X, padx=10, pady=5)

        self.page_info = ttk.Label(pagination_frame, text="Страница 1 из 1")
        self.page_info.pack(side=tk.LEFT, padx=5)

        ttk.Button(pagination_frame, text="<<",
                   command=self.controller.first_page).pack(side=tk.LEFT, padx=2)
        ttk.Button(pagination_frame, text="<",
                   command=self.controller.prev_page).pack(side=tk.LEFT, padx=2)
        ttk.Button(pagination_frame, text=">",
                   command=self.controller.next_page).pack(side=tk.LEFT, padx=2)
        ttk.Button(pagination_frame, text=">>",
                   command=self.controller.last_page).pack(side=tk.LEFT, padx=2)

        ttk.Label(pagination_frame, text="Записей на странице:").pack(side=tk.LEFT, padx=(20, 5))
        self.page_size_var = tk.StringVar(value="10")
        page_size_combo = ttk.Combobox(pagination_frame, textvariable=self.page_size_var,
                                       values=["5", "10", "20", "50"], width=5)
        page_size_combo.bind('<<ComboboxSelected>>',
                             lambda e: self.controller.change_page_size(int(self.page_size_var.get())))
        page_size_combo.pack(side=tk.LEFT)

        ttk.Button(pagination_frame, text="Все записи",
                   command=self.controller.show_all).pack(side=tk.LEFT, padx=10)

        self.total_label = ttk.Label(pagination_frame, text="Всего записей: 0")
        self.total_label.pack(side=tk.RIGHT, padx=5)

    def update_table(self, students):
        for row in self.table.get_children():
            self.table.delete(row)

        for student in students:
            self.table.insert('', tk.END, values=(
                f"{student.surname} {student.name} {student.patronymic}",
                student.course,
                student.group,
                student.total_number_of_works,
                student.number_of_completed_tasks,
                student.programming_language.value
            ))

    def update_pagination_info(self, current_page, total_pages, total_records):
        self.page_info.config(text=f"Страница {current_page} из {total_pages}")
        self.total_label.config(text=f"Всего записей: {total_records}")
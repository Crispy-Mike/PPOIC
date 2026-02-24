from tkinter import filedialog, messagebox
from model.xml_handler import XMLHandler

class XMLController:
    def __init__(self, main_controller):
        self.main_controller = main_controller

    def save_to_xml(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            try:
                XMLHandler.save_to_xml(self.main_controller.model.students, filename)
                messagebox.showinfo("Успех", "Данные успешно сохранены в XML")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить: {str(e)}")

    def load_from_xml(self):
        filename = filedialog.askopenfilename(
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            try:
                students = XMLHandler.load_from_xml(filename)
                self.main_controller.model.students = students
                self.main_controller.refresh_view()
                messagebox.showinfo("Успех", f"Загружено студентов: {len(students)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {str(e)}")
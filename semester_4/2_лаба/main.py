# main.py
from controller.main_controller import MainController

if __name__ == "__main__":
    controller = MainController()

    print(f"Всего студентов в модели: {len(controller.model.students)}")

    controller.run()
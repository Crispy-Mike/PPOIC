#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path

# Переименовываем импорт, чтобы избежать конфликта
try:
    from statemachine import StateMachine as SMStateMachine, State
    from statemachine.contrib.diagram import DotGraphMachine

    HAS_STATEMACHINE = True
except ImportError:
    HAS_STATEMACHINE = False
    print("Предупреждение: python-statemachine не установлен")
    print("Установите: pip install python-statemachine[diagrams]")


def check_graphviz():
    try:
        subprocess.run(['dot', '-V'], capture_output=True, check=True)
        return True
    except:
        return False


HAS_GRAPHVIZ = check_graphviz()

if HAS_STATEMACHINE:
    class StudentUMLStateMachine(SMStateMachine):
        created = State('Создание', initial=True)
        active = State('Активный')
        attending = State('Посещение занятий')
        studying = State('Изучение материалов')
        planning = State('Учебное планирование')
        examining = State('Подготовка к экзаменам')
        using_library = State('Использование библиотеки')
        saving = State('Сохранение данных')
        deleted = State('Удален', final=True)

        activate = created.to(active)
        start_attending = active.to(attending)
        finish_attending = attending.to(active)
        start_studying = active.to(studying)
        finish_studying = studying.to(active)
        start_planning = active.to(planning)
        finish_planning = planning.to(active)
        start_examining = active.to(examining)
        finish_examining = examining.to(active)
        start_library = active.to(using_library)
        finish_library = using_library.to(active)
        save_data = active.to(saving)
        saved = saving.to(active)
        delete = active.to(deleted)

        def __init__(self):
            super().__init__()
            self.activate.label = "Добавление студента"
            self.start_attending.label = "Операция 1: Посещение занятий"
            self.finish_attending.label = "Завершение отметок"
            self.start_studying.label = "Операция 2: Изучение материалов"
            self.finish_studying.label = "Завершение оценок"
            self.start_planning.label = "Операция 4: Учебное планирование"
            self.finish_planning.label = "Просмотр расписания"
            self.start_examining.label = "Операция 3: Подготовка к экзаменам"
            self.finish_examining.label = "Анализ успеваемости"
            self.start_library.label = "Операция 5: Использование библиотеки"
            self.finish_library.label = "Возврат/выдача книг"
            self.save_data.label = "Операция 6: Сохранить данные"
            self.saved.label = "Данные сохранены"
            self.delete.label = "Операция 8: Удаление студента"


def generate_state_diagram():
    print("\nГенерация диаграммы состояний...")

    if not HAS_STATEMACHINE:
        print("Ошибка: Не установлен python-statemachine")
        return False

    if not HAS_GRAPHVIZ:
        print("Предупреждение: Graphviz не найден, будет сгенерирован только DOT/SVG формат")

    try:
        # Создаем простую машину состояний без сложных атрибутов
        from statemachine import StateMachine

        class StudentStateMachine(StateMachine):
            "Конечный автомат студента"

            # Состояния
            created = State('Создание', initial=True)
            active = State('Активный')
            attending = State('Посещение занятий')
            studying = State('Изучение материалов')
            planning = State('Учебное планирование')
            examining = State('Подготовка к экзаменам')
            using_library = State('Использование библиотеки')
            saving = State('Сохранение данных')
            deleted = State('Удален', final=True)

            # Переходы
            activate = created.to(active)
            start_attending = active.to(attending)
            finish_attending = attending.to(active)
            start_studying = active.to(studying)
            finish_studying = studying.to(active)
            start_planning = active.to(planning)
            finish_planning = planning.to(active)
            start_examining = active.to(examining)
            finish_examining = examining.to(active)
            start_library = active.to(using_library)
            finish_library = using_library.to(active)
            save_data = active.to(saving)
            saved = saving.to(active)
            delete = active.to(deleted)

        # Создаем экземпляр
        machine = StudentStateMachine()

        # Генерируем граф
        graph = DotGraphMachine(machine)

        # Пытаемся установить атрибуты если они существуют
        try:
            graph.graph_attr.update({
                'rankdir': 'TB',
                'fontname': 'Arial',
                'label': 'Диаграмма состояний студента',
            })
        except AttributeError:
            pass  # Пропускаем если атрибут не существует

        try:
            graph.node_attr.update({
                'shape': 'box',
                'style': 'rounded,filled',
                'fillcolor': 'lightblue',
            })
        except AttributeError:
            pass

        # Сохраняем в разных форматах
        try:
            if HAS_GRAPHVIZ:
                graph.write_png('state_diagram.png')
                print("✓ Сгенерирован PNG: state_diagram.png")
        except Exception as e:
            print(f"Не удалось создать PNG: {e}")

        try:
            graph.write_svg('state_diagram.svg')
            print("✓ Сгенерирован SVG: state_diagram.svg")
        except Exception as e:
            print(f"Не удалось создать SVG: {e}")

        try:
            graph.write('state_diagram.dot')
            print("✓ Сгенерирован DOT: state_diagram.dot")
        except Exception as e:
            print(f"Не удалось создать DOT: {e}")

        # Дополнительно создаем текстовое описание
        state_text = """
ДИАГРАММА СОСТОЯНИЙ СТУДЕНТА
══════════════════════════════

[Начало] → Создание → Активный

Активный → Посещение занятий     (Операция 1)
Посещение занятий → Активный     (Завершение отметок)

Активный → Изучение материалов   (Операция 2)
Изучение материалов → Активный   (Завершение оценок)

Активный → Учебное планирование  (Операция 4)
Учебное планирование → Активный  (Просмотр расписания)

Активный → Подготовка к экзаменам (Операция 3)
Подготовка к экзаменам → Активный (Анализ успеваемости)

Активный → Использование библиотеки (Операция 5)
Использование библиотеки → Активный (Возврат/выдача книг)

Активный → Сохранение данных     (Операция 6)
Сохранение данных → Активный     (Данные сохранены)

Активный → Удален                 (Операция 8)
Удален → [Конец]
"""

        with open('state_diagram.txt', 'w', encoding='utf-8') as f:
            f.write(state_text)
        print("✓ Сгенерировано текстовое описание: state_diagram.txt")

        return True

    except Exception as e:
        print(f"Ошибка при генерации диаграммы состояний: {e}")
        # Создаем хотя бы текстовую версию
        try:
            state_text = """
ДИАГРАММА СОСТОЯНИЙ СТУДЕНТА (резервная копия)
══════════════════════════════════════════════

Начало → Создание → Активный

Активный → Посещение занятий (1)
Посещение занятий → Активный

Активный → Изучение материалов (2)
Изучение материалов → Активный

Активный → Учебное планирование (4)
Учебное планирование → Активный

Активный → Подготовка к экзаменам (3)
Подготовка к экзаменам → Активный

Активный → Использование библиотеки (5)
Использование библиотеки → Активный

Активный → Сохранение данных (6)
Сохранение данных → Активный

Активный → Удален (8)
Удален → Конец
"""
            with open('state_diagram.txt', 'w', encoding='utf-8') as f:
                f.write(state_text)
            print("✓ Создана текстовая диаграмма состояний")
            return True
        except:
            return False


def generate_class_diagram_pyreverse():
    print("\nГенерация диаграммы классов...")

    try:
        subprocess.run(['pyreverse', '--version'], capture_output=True, check=True)
    except:
        print("Ошибка: Pyreverse не найден. Установите pylint:")
        print("pip install pylint")
        return False

    try:
        current_dir = os.getcwd()
        parent_dir = str(Path(current_dir).parent)

        result = subprocess.run(
            ['pyreverse', '-o', 'png', '-p', 'StudentModel', parent_dir],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        if os.path.exists('classes_StudentModel.png'):
            os.rename('classes_StudentModel.png', 'class_diagram.png')
            print("✓ Сгенерирована диаграмма классов: class_diagram.png")
        else:
            print("Не удалось найти сгенерированный файл classes_StudentModel.png")

        if os.path.exists('packages_StudentModel.png'):
            os.rename('packages_StudentModel.png', 'packages_diagram.png')
            print("✓ Сгенерирована диаграмма пакетов: packages_diagram.png")

        return True

    except Exception as e:
        print(f"Ошибка при генерации диаграммы классов: {e}")
        return False


def generate_class_diagram_text():
    print("\nГенерация текстового описания диаграммы классов...")

    class_diagram_text = """
Диаграмма классов (текстовое описание):

┌─────────────────────────────────┐
│           AllStudents           │
├─────────────────────────────────┤
│ - students: List[Student]       │
│ - library: Library               │
├─────────────────────────────────┤
│ + new_student()                  │
│ + delete_student()               │
│ + redact_student()               │
│ + save_data()                    │
│ + load_data()                    │
│ + clear_data()                   │
│ + visit_of_last_week()           │
│ + material_study_operation()     │
│ + exam_preparation_operation()   │
│ + curricular_planning_operation()│
│ + operation_of_using_library()   │
│ + new_book()                      │
└─────────────────────────────────┘
               │
               │ 1..* (содержит)
               ▼
┌─────────────────────────────────┐
│            Student               │
├─────────────────────────────────┤
│ - name: str                      │
│ - surname: str                   │
│ - group: str                      │
│ - specialty: str                  │
│ - educational_materials: List     │
│ - exams: List                    │
│ - schedule: Dict                  │
│ - visits: Dict                    │
│ - marks: Dict                     │
│ - books: List[Book]               │
├─────────────────────────────────┤
│ + get_information()               │
│ + get_schedule()                  │
│ + new_visit()                     │
│ + get_visit()                     │
│ + new_marks()                     │
│ + get_marks()                     │
│ + exam_check()                    │
└─────────────────────────────────┘
               │
               │ 0..* (имеет)
               ▼
┌─────────────────────────────────┐
│             Book                 │
├─────────────────────────────────┤
│ - name_of_book: str              │
│ - name_of_author: str            │
│ - genre: str                      │
│ - content: str                    │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│            Library               │
├─────────────────────────────────┤
│ - books: List[Book]              │
├─────────────────────────────────┤
│ + new_book()                      │
│ + redact()                        │
│ + delete_book()                   │
└─────────────────────────────────┘
               │
               │ 1 (содержит)
               ▼
┌─────────────────────────────────┐
│             Book                 │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│         GlobalVariables         │
├─────────────────────────────────┤
│ + DAYS: List[str]                │
│ + TIME_OF_CLASSES: List[str]     │
└─────────────────────────────────┘

Отношения:
- AllStudents содержит множество Students (композиция)
- AllStudents содержит одну Library (композиция)
- Library содержит множество Books (агрегация)
- Student может иметь множество Books (ассоциация)
- Student и Library используют GlobalVariables (зависимость)
"""

    try:
        with open('class_diagram_text.txt', 'w', encoding='utf-8') as f:
            f.write(class_diagram_text)
        print("✓ Сгенерировано текстовое описание: class_diagram_text.txt")
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def generate_plantuml_diagram():
    print("\nГенерация PlantUML диаграммы...")

    plantuml_code = """@startuml
title Диаграмма классов - Модель студента

class Student {
    - name: str
    - surname: str
    - group: str
    - specialty: str
    - educational_materials: List[str]
    - exams: List[str]
    - schedule: Dict[str, List[str]]
    - visits: Dict[str, List[str]]
    - marks: Dict[str, List[int]]
    - books: List[Book]
    --
    + get_information(): None
    + get_schedule(): None
    + new_visit(): None
    + get_visit(): None
    + new_marks(): None
    + get_marks(): None
    + exam_check(): Dict
}

class Book {
    - name_of_book: str
    - name_of_author: str
    - genre: str
    - content: str
    --
    + __init__(name, author, genre, content)
}

class Library {
    - books: List[Book]
    --
    + new_book(): None
    + redact(name, author): None
    + delete_book(name, author): None
}

class AllStudents {
    - students: List[Student]
    - library: Library
    --
    + new_student(): None
    + delete_student(): None
    + redact_student(): None
    + save_data(filename: str): None
    + load_data(filename: str): None
    + clear_data(): None
    + visit_of_last_week(): None
    + material_study_operation(): None
    + exam_preparation_operation(): None
    + curricular_planning_operation(): None
    + operation_of_using_library_resources(): None
    + new_book(): None
}

class GlobalVariables {
    + {static} DAYS: List[str]
    + {static} TIME_OF_CLASSES: List[str]
}

AllStudents "1" *-- "0..*" Student : содержит
AllStudents "1" *-- "1" Library : управляет
Library "1" o-- "0..*" Book : хранит
Student "1" --> "0..*" Book : берет
Student ..> GlobalVariables : использует
Library ..> GlobalVariables : использует

note top of Student : Основная сущность системы
note right of AllStudents : Контроллер системы
@enduml
"""

    try:
        with open('class_diagram.plantuml', 'w', encoding='utf-8') as f:
            f.write(plantuml_code)
        print("✓ Сгенерирован PlantUML файл: class_diagram.plantuml")
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def main():
    print("\n" + "=" * 50)
    print("ГЕНЕРАТОР UML ДИАГРАММ")
    print("=" * 50)

    diagrams_dir = Path('diagrams')
    diagrams_dir.mkdir(exist_ok=True)

    original_dir = os.getcwd()
    os.chdir(diagrams_dir)

    results = []

    print("\n1. Генерация диаграммы состояний...")
    state_result = generate_state_diagram()
    results.append(("Диаграмма состояний", state_result))

    print("\n2. Генерация диаграммы классов (Pyreverse)...")
    class_result = generate_class_diagram_pyreverse()
    results.append(("Диаграмма классов (Pyreverse)", class_result))

    print("\n3. Генерация текстовой диаграммы классов...")
    text_result = generate_class_diagram_text()
    results.append(("Текстовая диаграмма", text_result))

    print("\n4. Генерация PlantUML диаграммы...")
    plantuml_result = generate_plantuml_diagram()
    results.append(("PlantUML диаграмма", plantuml_result))

    os.chdir(original_dir)

    print("\n" + "=" * 50)
    print("ИТОГ ГЕНЕРАЦИИ:")
    print("=" * 50)

    all_success = True
    for name, success in results:
        status = "✓ УСПЕХ" if success else "✗ ОШИБКА"
        print(f"{name}: {status}")
        if not success:
            all_success = False

    if all_success:
        print("\n✅ Все диаграммы сгенерированы в папке 'diagrams/'")
    else:
        print("\n⚠️ Некоторые диаграммы не удалось сгенерировать")
        print("\nДля полной генерации установите:")
        print("pip install pylint python-statemachine[diagrams]")
        print("Скачайте Graphviz с https://graphviz.org/download/")


if __name__ == '__main__':
    main()
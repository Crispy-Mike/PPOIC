#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Добавляем путь к общему коду
sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))

# В app.py
from All_Students import All_Students
from Student import Student
from Global_variables import DAYS, TIME_OF_CLASSES
from exceptions.empty_name_error import EmptyNameError
from exceptions.invalid_mark_error import InvalidMarkError
from exceptions.visit_not_marked_error import VisitNotMarkedError
from exceptions.day_not_found_error import DayNotFoundError


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Для flash сообщений

# Глобальный объект для хранения данных
all_students = All_Students()


    @app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html',
                           students_count=len(all_students.students),
                           books_count=len(all_students.library.books))


@app.route('/students')
def students_list():
    """Список всех студентов"""
    return render_template('students.html',
                           students=all_students.students,
                           days=DAYS)


@app.route('/student/<int:student_id>')
def student_detail(student_id):
    """Детальная информация о студенте"""
    if 0 <= student_id < len(all_students.students):
        student = all_students.students[student_id]
        return render_template('student_detail.html',
                               student=student,
                               student_id=student_id,
                               days=DAYS,
                               time_slots=TIME_OF_CLASSES)
    flash('Студент не найден', 'error')
    return redirect(url_for('students_list'))


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    """Добавление нового студента"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            surname = request.form['surname']
            group = request.form['group']
            specialty = request.form['specialty']

            # Получаем учебные материалы
            materials = request.form.getlist('materials[]')
            materials = [m for m in materials if m.strip()]

            # Получаем экзамены
            exams = request.form.getlist('exams[]')
            exams = [e for e in exams if e.strip()]

            # Создаем студента
            student = Student(name, surname, group, specialty)
            student.educational_materials = materials
            student.exams = exams

            # Инициализируем расписание
            student.schedule = {}
            for day in DAYS:
                student.schedule[day] = ["-"] * len(TIME_OF_CLASSES)

            all_students.students.append(student)
            all_students.save_data()

            flash(f'Студент {name} {surname} успешно добавлен!', 'success')
            return redirect(url_for('students_list'))

        except EmptyNameError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')

    return render_template('add_student.html',
                           days=DAYS,
                           time_slots=TIME_OF_CLASSES)


@app.route('/student/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    """Редактирование студента"""
    if not (0 <= student_id < len(all_students.students)):
        flash('Студент не найден', 'error')
        return redirect(url_for('students_list'))

    student = all_students.students[student_id]

    if request.method == 'POST':
        try:
            student.name = request.form['name']
            student.surname = request.form['surname']
            student.group = request.form['group']
            student.specialty = request.form['specialty']

            # Обновляем учебные материалы
            materials = request.form.getlist('materials[]')
            student.educational_materials = [m for m in materials if m.strip()]

            # Обновляем экзамены
            exams = request.form.getlist('exams[]')
            student.exams = [e for e in exams if e.strip()]

            all_students.save_data()
            flash('Данные студента обновлены!', 'success')
            return redirect(url_for('student_detail', student_id=student_id))

        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')

    return render_template('edit_student.html',
                           student=student,
                           student_id=student_id)


@app.route('/student/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    """Удаление студента"""
    if 0 <= student_id < len(all_students.students):
        student = all_students.students.pop(student_id)
        all_students.save_data()
        flash(f'Студент {student.name} {student.surname} удален', 'success')
    else:
        flash('Студент не найден', 'error')
    return redirect(url_for('students_list'))


@app.route('/student/<int:student_id>/visit', methods=['GET', 'POST'])
def manage_visit(student_id):
    """Управление посещаемостью"""
    if not (0 <= student_id < len(all_students.students)):
        flash('Студент не найден', 'error')
        return redirect(url_for('students_list'))

    student = all_students.students[student_id]

    if request.method == 'POST':
        try:
            # Обрабатываем посещаемость
            visits = {}
            for day in DAYS:
                day_visits = []
                for i, time in enumerate(TIME_OF_CLASSES):
                    key = f"visit_{day}_{i}"
                    if key in request.form:
                        day_visits.append(request.form[key])
                    else:
                        day_visits.append("-")
                visits[day] = day_visits

            student.visits = visits
            all_students.save_data()
            flash('Посещаемость сохранена!', 'success')
            return redirect(url_for('student_detail', student_id=student_id))

        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')

    return render_template('visit.html',
                           student=student,
                           student_id=student_id,
                           days=DAYS,
                           time_slots=TIME_OF_CLASSES)


@app.route('/student/<int:student_id>/marks', methods=['GET', 'POST'])
def manage_marks(student_id):
    """Управление оценками"""
    if not (0 <= student_id < len(all_students.students)):
        flash('Студент не найден', 'error')
        return redirect(url_for('students_list'))

    student = all_students.students[student_id]

    try:
        if not student.visits:
            raise VisitNotMarkedError()
    except VisitNotMarkedError as e:
        flash(str(e), 'error')
        return redirect(url_for('student_detail', student_id=student_id))

    if request.method == 'POST':
        try:
            # Обрабатываем оценки
            marks = {}
            for day in DAYS:
                day_marks = []
                for i, time in enumerate(TIME_OF_CLASSES):
                    key = f"mark_{day}_{i}"
                    if key in request.form and request.form[key]:
                        mark = int(request.form[key])
                        if 1 <= mark <= 10:
                            day_marks.append(mark)
                        else:
                            day_marks.append("-")
                    else:
                        day_marks.append("-")
                marks[day] = day_marks

            student.marks = marks
            all_students.save_data()
            flash('Оценки сохранены!', 'success')
            return redirect(url_for('student_detail', student_id=student_id))

        except ValueError:
            flash('Оценка должна быть числом от 1 до 10', 'error')
        except InvalidMarkError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')

    return render_template('marks.html',
                           student=student,
                           student_id=student_id,
                           days=DAYS,
                           time_slots=TIME_OF_CLASSES)


@app.route('/student/<int:student_id>/schedule', methods=['GET', 'POST'])
def edit_schedule(student_id):
    """Редактирование расписания"""
    if not (0 <= student_id < len(all_students.students)):
        flash('Студент не найден', 'error')
        return redirect(url_for('students_list'))

    student = all_students.students[student_id]

    if request.method == 'POST':
        try:
            schedule = {}
            for day in DAYS:
                day_schedule = []
                for i, time in enumerate(TIME_OF_CLASSES):
                    key = f"schedule_{day}_{i}"
                    subject = request.form.get(key, "")
                    if subject and subject in student.educational_materials:
                        day_schedule.append(subject)
                    else:
                        day_schedule.append("-" if not subject else subject)
                schedule[day] = day_schedule

            student.schedule = schedule
            all_students.save_data()
            flash('Расписание обновлено!', 'success')
            return redirect(url_for('student_detail', student_id=student_id))

        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')

    return render_template('schedule.html',
                           student=student,
                           student_id=student_id,
                           days=DAYS,
                           time_slots=TIME_OF_CLASSES)


@app.route('/library')
def library():
    """Библиотека"""
    return render_template('library.html',
                           library=all_students.library,
                           students=all_students.students)


@app.route('/library/add_book', methods=['POST'])
def add_book():
    """Добавление книги в библиотеку"""
    try:
        name = request.form['name']
        author = request.form['author']
        genre = request.form['genre']
        content = request.form['content']

        from Book import Book
        book = Book(name, author, genre, content)
        all_students.library.books.append(book)
        all_students.save_data()

        flash(f'Книга "{name}" добавлена!', 'success')
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')

    return redirect(url_for('library'))


@app.route('/library/borrow_book', methods=['POST'])
def borrow_book():
    """Выдача книги студенту"""
    try:
        student_id = int(request.form['student_id'])
        book_id = int(request.form['book_id'])

        if 0 <= student_id < len(all_students.students):
            student = all_students.students[student_id]
            if 0 <= book_id < len(all_students.library.books):
                book = all_students.library.books.pop(book_id)
                student.books.append(book)
                all_students.save_data()
                flash(f'Книга выдана студенту {student.name} {student.surname}', 'success')
            else:
                flash('Книга не найдена', 'error')
        else:
            flash('Студент не найден', 'error')
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')

    return redirect(url_for('library'))


@app.route('/library/return_book', methods=['POST'])
def return_book():
    """Возврат книги в библиотеку"""
    try:
        student_id = int(request.form['student_id'])
        book_id = int(request.form['book_id'])

        if 0 <= student_id < len(all_students.students):
            student = all_students.students[student_id]
            if 0 <= book_id < len(student.books):
                book = student.books.pop(book_id)
                all_students.library.books.append(book)
                all_students.save_data()
                flash(f'Книга возвращена в библиотеку', 'success')
            else:
                flash('Книга не найдена у студента', 'error')
        else:
            flash('Студент не найден', 'error')
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')

    return redirect(url_for('library'))


@app.route('/clear_data', methods=['POST'])
def clear_data():
    """Очистка всех данных"""
    confirm = request.form.get('confirm', '')
    if confirm.lower() in ['да', 'yes', '1']:
        all_students.clear_data()
        flash('Все данные удалены', 'success')
    else:
        flash('Очистка отменена', 'info')
    return redirect(url_for('index'))


@app.route('/save_data')
def save_data():
    """Сохранение данных"""
    all_students.save_data()
    flash('Данные сохранены', 'success')
    return redirect(request.referrer or url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
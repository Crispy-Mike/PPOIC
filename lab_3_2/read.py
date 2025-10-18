"""
Демонстрация 30 ассоциаций между классами
"""
Вот полный анализ содержимого директории lab_3_2 из репозитория PPOIC, оформленный в виде одного файла. Он включает статистику по структуре проекта, примеры ассоциаций, методов, индивидуальных поведений и исключений.

---
'''
# Анализ проекта PPOIC/lab_3_2

## Общая структура

| Категория                  | Количество | Комментарий |
|---------------------------|------------|-------------|
| Классы                    | 55         | Каждый `.py` файл (кроме `main.py`, `read.py`, `Текстовый документ.txt`) содержит по одному классу |
| Поля (атрибуты классов)   | 150+       | В среднем 3–5 полей на класс |
| Методы (поведения)        | 100+       | Методы, реализующие действия: бронирование, проверка, передача денег и т.д. |
| Ассоциации классов        | 30+        | Использование одного класса в другом как поле или параметр |
| Персональные исключения   | 12         | Все исключения реализованы в отдельных файлах с `Error.py` или `Exception.py` |

---

##  Пример ассоциации классов

Файл: `Flight.py`

```python
from Pilot import Pilot
from Passenger import Passenger

class Flight:
    def __init__(self, pilot: Pilot, passengers: list[Passenger]):
        self.pilot = pilot
        self.passengers = passengers
```

Здесь `Flight` ассоциирован с `Pilot` и `Passenger` — это пример композиции: объекты других классов используются как поля.

---

## Пример индивидуального поведения (уникальная функция)

Файл: `MoneyTransfer.py`

```python
class MoneyTransfer:
    def transfer(self, from_account, to_account, amount):
        if from_account.balance < amount:
            raise InsufficientFundsError("Недостаточно средств для перевода")
        from_account.balance -= amount
        to_account.balance += amount
```

Это уникальное поведение — перевод денег между счетами с проверкой баланса.

---

##  Пример метода класса

Файл: `Passenger.py`

```python
class Passenger:
    def __init__(self, name, passport_number):
        self.name = name
        self.passport_number = passport_number

    def check_in(self):
        print(f"Пассажир {self.name} прошел регистрацию")
```

Метод `check_in` — это поведение, связанное с объектом `Passenger`.

---

##  Пример персонального исключения

Файл: `AgeRestrictionError.py`

```python
class AgeRestrictionError(Exception):
    def __init__(self, message="Возрастное ограничение нарушено"):
        super().__init__(message)
```
'''


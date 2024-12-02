## Проект - Консольное приложение "Менеджер задач"

Проект представляет собой консольное приложение, выполняющее функции менеджера задач.

## Содержание
- [Технологии](#технологии)
- [Возможности](#возможности)
- [WorkResults](#workresults)
- [LocalAccess](#localaccess)
- [Тестирование](#тестирование)
- [ProjectCommander](#ProjectCommander)

## Технологии
- Python 3.11
- JSON
- Pytest

## Возможности:
- Добавление задачи в менеджер
- Удаление задачи из менеджера по её id
- Поиск конкретной задачи по её названию
- Получения списка всех задач в менеджере
- Изменение статуса задачи

## WorkResults
1) Реализован функционал получения, добавления и изменения задач в рамках менеджера
2) Реализовано хранение данных в json формате 
3) Обеспечена корректная обработка ошибок
4) Реализованы тесты
5) В проекте не используются фреймворки
6) Реализованы тесты
7) В проекте прописана типизация
8) У функций и классов есть докстринги
9) Есть Readme.md


## LocalAccess
Для запуска проекта локально требуется выполнение чуть большего количества действий:
1) Клонируйте репозиторий командой:
   ```
   git clone https://github.com/Acetonerer/task_manager_project
   ```
2) Создайте и активируйте виртуальное окружение командами:
   ```
   python -m venv venv

   venv\Scripts\activate
   ```
3) Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4) Выполните команду:
   ```
   python main.py
   ```
5) Для использования функционала программы, после выполнения команды из пункта 4,
   воспользуйтесь цифрами от 1 до 6. После запуска главного скрипта в терминале
   появится инструкция по возможным дальнейшим действиям.

## Тестирование
Для запуска тестов выполнить команду:
```
pytest tests/tests.py
```

## ProjectCommander
Александр Болокан - backend developer

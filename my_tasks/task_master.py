from typing import List, Dict
import json
from .logger import log, success, error
import datetime


class Task:
    """
    Класс, собственно, задачи
    """
    def __init__(self, task_id: int, title: str, description: str, category: str,
                 priority: str, date_create=datetime.datetime.now().strftime("%d.%m.%Y"), status: str = "Не выполнена"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.status = status
        self.priority = priority
        self.date_create = date_create

    def __str__(self) -> str:
        """
        Строковое представление задачи

        :return: Строка с данными о задаче
        """
        return (
            f"ID: {self.task_id} "
            f"| Название: {self.title} "
            f"| Описание: {self.description} "
            f"| Категория: {self.category} "
            f"| Дата создания: {self.date_create}"
            f"| Приоритетность: {self.priority}"
            f"| Статус: {self.status}"
            )

    def to_dict(self) -> Dict:
        """
        Преобразует объект задачи в словарь

        :return: Словарь с данными задачи
        """
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "date_create": self.date_create,
            "priority": self.priority,
            "status": self.status,
        }


class TaskManager:
    """
    Класс, собственно, менеджера задач
    """
    def __init__(self, storage_file: str):
        """
        Инициализация библиотеки с загрузкой данных из файла

        :param storage_file: Путь к файлу с данными
        """
        self.storage_file = storage_file
        self.tasks: List[Task] = self.load_from_database()

    def load_from_database(self) -> List[Task]:
        """
        Метод загрузки данных из БД и преобразования их в объекты класса Task

        :return: Список объектов Task
        """
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                log(f"Загружено {len(data)} задач из базы данных.")
                return [Task(**task_data) for task_data in data]
        except FileNotFoundError:
            log(f"Файл {self.storage_file} не найден. Создается новый пустой список.")
            return []
        except json.JSONDecodeError:
            error(f"Ошибка чтения файла {self.storage_file}. Проверьте его формат.")
            return []

    def save_to_storage(self):
        """
        Метод сохранения данных в БД в формате JSON
        """
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as file:
                json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)
        except Exception as e:
            error(f"Ошибка сохранения данных в файл {self.storage_file}: {e}")

    def add_task(self, title: str, description: str, category: str, priority: str):
        """
        Метод добавления новой задачи в БД
        :param title: Название задачи
        :param description:
        :param priority:
        :param category:
        """
        next_id = max([task.task_id for task in self.tasks], default=0) + 1
        new_task = Task(task_id=next_id, title=title, description=description,
                        category=category, priority=priority)
        self.tasks.append(new_task)
        self.save_to_storage()
        success(f"Задача с параметрами {new_task} \n       была успешно добавлена")

    def remove_task(self, task_id: int):
        """
        Метод удаления задачи по её task_id

        :param task_id: ID задачи
        """
        task_for_del = next((task for task in self.tasks if task.task_id == task_id), None)
        if task_for_del:
            self.tasks.remove(task_for_del)
            self.save_to_storage()
            success(f"Задача с ID {task_id} удалена")
        else:
            error(f"Задача с ID {task_id} не найдена")

    def search_tasks(self, query: str) -> List[Task]:
        """
        Метод поиска задачи в БД по её title

        :param query: Строка, по которой будет произведен поиск
        :return: Список задач, соответствующих запросу.
        """
        query = str(query).lower()

        found_books = [
            task for task in self.tasks
            if query in task.title.lower()
        ]
        if found_books:
            log(f"Найдено {len(found_books)} задач: ")
            for book in found_books:
                log(str(book))
        else:
            error(f"Задач по запросу '{query}' не найдено.")
        return found_books

    def list_tasks(self) -> List[Task]:
        """
        Метод отображения списка всех задач в БД

        :return: Список объектов Task
        """
        return self.tasks

    def update_task(self, task_id: int, **kwargs):
        """
        Метод для изменения задачи

        :param task_id: ID задачи, которую нужно изменить
        :param kwargs: Ключевые аргументы, соответствующие атрибутам задачи, которые нужно обновить
        """
        task = next((task for task in self.tasks if task.task_id == task_id), None)

        valid_fields = {'title', 'description', 'category', 'priority', 'status'}

        for field, value in kwargs.items():
            if field not in valid_fields:
                error(f"Недопустимое поле '{field}'. Допустимые поля: {valid_fields}.")
                continue

            if field == 'status' and value not in {'Не выполнена', 'Выполнена'}:
                error(f"Некорректный статус '{value}'. Допустимые статусы: 'Не выполнена', 'Выполнена'.")
                continue

            old_value = getattr(task, field, None)
            setattr(task, field, value)
            success(f"Поле '{field}' задачи (ID: {task_id}) обновлено с '{old_value}' на '{value}'.")

        self.save_to_storage()
        success(f"Задача с ID {task_id} успешно обновлена.")

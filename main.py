from my_tasks.task_master import TaskManager
from my_tasks.logger import log, error


def main():
    try:
        task_manager = TaskManager("my_tasks/database.json")
        while True:
            log("\nДоступные команды:")
            log("1. Добавить задачу")
            log("2. Удалить задачу")
            log("3. Найти задачу")
            log("4. Показать все задачи")
            log("5. Изменить задачу")
            log("6. Выйти")

            command = input("Введите номер команды: ").strip()

            if command == "1":
                title = input("Введите название задачи: ").strip()
                description = input("Введите описание задачи: ").strip()
                category = input("Введите категорию задачи: ").strip()
                priority = input("Введите приоритетность задачи: ").strip()

                task_manager.add_task(title, description, category, priority)

            elif command == "2":
                try:
                    task_id = int(input("Введите ID задачи: ").strip())
                    task_manager.remove_task(task_id)
                except ValueError:
                    error("Ошибка: ID задачи должно быть числом.")

            elif command == "3":
                query = input("Введите поисковый запрос (название): ").strip()
                task_manager.search_tasks(query)

            elif command == "4":
                tasks = task_manager.list_tasks()
                if tasks:
                    log("\nСписок задач:")
                    for task in tasks:
                        log(str(task))
                else:
                    error("База данных пуста.")

            elif command == "5":
                try:
                    task_id = int(input("Введите ID задачи: ").strip())

                    task = next(
                        (
                            task
                            for task in task_manager.tasks
                            if task.task_id == task_id
                        ),
                        None,
                    )

                    if not task:
                        error(f"Задача с ID {task_id} не найдена. Попробуйте снова.")
                    else:
                        print(
                            "Вы можете изменить следующие параметры задачи: title, "
                            "description, category, priority, status."
                        )
                        print("Оставьте поле пустым, если не хотите изменять значение.")

                        new_title = input(
                            f"Новое название задачи (текущее: '{task.title}'): "
                        ).strip()
                        new_description = input(
                            f"Новое описание задачи (текущее: '{task.description}'): "
                        ).strip()
                        new_category = input(
                            f"Новая категория задачи (текущая: '{task.category}'): "
                        ).strip()
                        new_priority = input(
                            f"Новая приоритетность задачи (текущая: '{task.priority}'): "
                        ).strip()
                        new_status = input(
                            f"Новый статус ('Не выполнена' или 'Выполнена', текущий: '{task.status}'): "
                        ).strip()

                        updates = {}
                        if new_title:
                            updates["title"] = new_title
                        if new_description:
                            updates["description"] = new_description
                        if new_category:
                            updates["category"] = new_category
                        if new_priority:
                            updates["priority"] = new_priority
                        if new_status:
                            updates["status"] = new_status

                        if updates:
                            task_manager.update_task(task_id, **updates)
                        else:
                            log("Изменения не внесены!.")
                except ValueError:
                    error("Ошибка: ID задачи должно быть числом.")

            elif command == "6":
                log("Выход из программы. До свидания!")
                break
            else:
                error("Ошибка: Некорректная команда. Попробуйте снова.")

    except KeyboardInterrupt:
        error("\nПрограмма прервана пользователем.")
    except Exception:
        error(f"Что-то произошло при выходе из программы:D")


if __name__ == "__main__":
    main()

import os
import pytest
from my_tasks.task_master import TaskManager


TEST_STORAGE_FILE = "test_tasks.json"


@pytest.fixture
def task_manager():
    if os.path.exists(TEST_STORAGE_FILE):
        os.remove(TEST_STORAGE_FILE)
    return TaskManager(storage_file=TEST_STORAGE_FILE)


def test_add_task(task_manager):
    """
    Тест на добавление новой задачи
    :param task_manager:
    :return:
    """
    task_manager.add_task(
        title="Test Task",
        description="Description of the test task",
        category="Work",
        priority="High"
    )
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Test Task"
    assert task_manager.tasks[0].status == "Не выполнена"


def test_update_task_status(task_manager):
    """
    Тест на обновленое статуса задачи
    :param task_manager:
    :return:
    """
    task_manager.add_task(
        title="Test Task",
        description="Description of the test task",
        category="Work",
        priority="High"
    )
    task_id = task_manager.tasks[0].task_id
    task_manager.update_task(task_id, status="Выполнена")
    assert task_manager.tasks[0].status == "Выполнена"


def test_search_tasks(task_manager):
    """
    Тест на поиск задачи
    :param task_manager:
    :return:
    """
    task_manager.add_task(
        title="Test Task 1",
        description="Description of task 1",
        category="Work",
        priority="High"
    )
    task_manager.add_task(
        title="Another Task",
        description="Description of another task",
        category="Personal",
        priority="Low"
    )
    found_tasks = task_manager.search_tasks("Test")
    assert len(found_tasks) == 1
    assert found_tasks[0].title == "Test Task 1"


def test_remove_task(task_manager):
    """
    Тест на удаление задачи
    :param task_manager:
    :return:
    """
    task_manager.add_task(
        title="Test Task",
        description="Description of the test task",
        category="Work",
        priority="High"
    )
    task_id = task_manager.tasks[0].task_id
    task_manager.remove_task(task_id)
    assert len(task_manager.tasks) == 0


def test_save_and_load(task_manager):
    """
    Тест на сохранение и загрузку данных
    :param task_manager:
    :return:
    """
    task_manager.add_task(
        title="Test Task",
        description="Description of the test task",
        category="Work",
        priority="High"
    )
    task_manager.save_to_storage()

    new_task_manager = TaskManager(storage_file=TEST_STORAGE_FILE)
    assert len(new_task_manager.tasks) == 1
    assert new_task_manager.tasks[0].title == "Test Task"


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    if os.path.exists(TEST_STORAGE_FILE):
        os.remove(TEST_STORAGE_FILE)

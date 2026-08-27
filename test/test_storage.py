from models import Task
import storage


def test_save_and_load_tasks(tmp_path, monkeypatch):
    test_file = tmp_path / "test_tasks.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    tasks = [
        Task(1, "学习 Python", priority="high"),
        Task(2, "学习 pytest", done=True),
    ]

    storage.save_tasks(tasks)
    loaded_tasks = storage.load_tasks()

    assert loaded_tasks == tasks


def test_load_when_file_not_exists(tmp_path, monkeypatch):
    test_file = tmp_path / "not_exists.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    assert storage.load_tasks() == []
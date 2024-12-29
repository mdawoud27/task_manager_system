import json
from datetime import datetime
from .models import Task


class TaskStorage:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, "w") as f:
            tasks_data = [task.to_dict() for task in self.tasks]
            json.dump(tasks_data, f, indent=2)

    def task_exists(self, title):
        """Check if a task with the given title already exists"""
        return any(task.title.lower() == title.lower() for task in self.tasks)

    def add_task(self, task):
        if not self.task_exists(task.title):
            self.tasks.append(task)
            self.save_tasks()
            return True
        return False

    def delete_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            self.save_tasks()

    def get_all_tasks(self):
        # Sort tasks by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.tasks, key=lambda x: priority_order[x.priority.lower()])

    def get_pending_tasks(self):
        tasks = [task for task in self.tasks if not task.completed]
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda x: priority_order[x.priority.lower()])

    def get_completed_tasks(self):
        tasks = [task for task in self.tasks if task.completed]
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda x: priority_order[x.priority.lower()])

    def mark_task_complete(self, index):
        pending_tasks = self.get_pending_tasks()
        if 0 <= index < len(pending_tasks):
            task = pending_tasks[index]
            task.mark_complete()
            self.save_tasks()
            return True
        return False

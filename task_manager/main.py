"""Main entry point for the Task Manager application"""

from .models import Task
from .storage import TaskStorage


class TaskManager:
    def __init__(self):
        self.storage = TaskStorage()

    def create_task(self, title, description, due_date=None, priority="low"):
        """Create a new task with validation"""
        if self.storage.task_exists(title):
            return None

        task = Task(title, description, due_date, priority)
        self.storage.add_task(task)
        self.storage.save_tasks()
        return task


def main():
    """Entry point for CLI mode"""
    from .cli.interface import CLI

    task_manager = TaskManager()
    cli = CLI(task_manager)
    cli.run()


if __name__ == "__main__":
    main()

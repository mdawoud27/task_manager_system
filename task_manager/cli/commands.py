"""CLI commands implementation"""

from datetime import datetime


class CLICommands:
    def __init__(self, task_manager):
        self.task_manager = task_manager

    def add_task(self):
        """Add a new task through CLI"""
        print("\n=== Add New Task ===")
        title = input("Enter task title: ").strip()

        # Check if task exists
        if self.task_manager.storage.task_exists(title):
            print("Error: A task with this title already exists!")
            return

        description = input("Enter task description: ").strip()
        due_date_str = input(
            "Enter due date (YYYY-MM-DD) or press Enter to skip: "
        ).strip()
        priority = (
            input("Enter priority (low/medium/high) [medium]: ").lower().strip()
            or "medium"
        )

        # Validate priority
        if priority not in ["low", "medium", "high"]:
            print("Invalid priority! Using 'medium' as default.")
            priority = "medium"

        # Parse due date
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format! Due date will not be set.")

        # Create and add task
        task = self.task_manager.create_task(title, description, due_date, priority)
        if task:
            print("Task added successfully!")

    def view_tasks(self, tasks, title="Tasks"):
        """Display tasks in a formatted way"""
        if not tasks:
            print("\nNo tasks found!")
            return

        print(f"\n=== {title} ===")
        for i, task in enumerate(tasks, 1):
            status = "✓" if task.completed else "○"
            due_date = (
                task.due_date.strftime("%Y-%m-%d") if task.due_date else "No due date"
            )
            print(f"\n{i}. [{status}] {task.title}")
            print(f"   Description: {task.description}")
            print(f"   Priority: {task.priority}")
            print(f"   Due Date: {due_date}")

    def mark_task_complete(self):
        """Mark a task as complete"""
        pending_tasks = self.task_manager.storage.get_pending_tasks()

        if not pending_tasks:
            print("\nNo pending tasks!")
            return

        print("\n=== Pending Tasks ===")
        for i, task in enumerate(pending_tasks, 1):
            print(f"{i}. {task.title}")

        try:
            choice = input("\nEnter task number to mark as complete: ").strip()
            if not choice.isdigit():
                print("Please enter a valid number!")
                return

            index = int(choice) - 1
            if 0 <= index < len(pending_tasks):
                task = pending_tasks[index]
                task.mark_complete()
                self.task_manager.storage.save_tasks()
                print("Task marked as complete!")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

import tkinter as tk
from tkinter import ttk, messagebox
from .task_form import TaskForm
from .task_list import TaskList
from .styles import configure_styles


class MainWindow(tk.Tk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.title("Task Manager")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(1024, 768)
        configure_styles()

    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tasks tab
        self.tasks_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tasks_frame, text="Active Tasks")

        # Archive tab
        self.archive_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.archive_frame, text="Archive")

        # Add task form to active tasks tab
        self.task_form = TaskForm(self.tasks_frame, self.on_task_submit)
        self.task_form.pack(fill=tk.X, padx=5, pady=(5, 10))

        # Add separator
        ttk.Separator(self.tasks_frame, orient="horizontal").pack(
            fill=tk.X, padx=5, pady=5
        )

        # Add task lists
        self.active_task_list = TaskList(self.tasks_frame)
        self.active_task_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.archive_task_list = TaskList(self.archive_frame)
        self.archive_task_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add control buttons
        self.create_control_buttons(self.tasks_frame)
        self.create_archive_buttons(self.archive_frame)

        # Update task lists
        self.update_task_lists()

    def create_control_buttons(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            btn_frame,
            text="Mark Complete",
            command=self.mark_selected_complete,
            style="Action.TButton",
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Edit Task",
            command=self.edit_selected_task,
            style="Action.TButton",
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Delete Task",
            command=self.delete_active_task,
            style="Danger.TButton",
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(btn_frame, text="Refresh", command=self.refresh_lists).pack(
            side=tk.LEFT, padx=5
        )

    def create_archive_buttons(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            btn_frame,
            text="Restore Task",
            command=self.restore_selected_task,
            style="Action.TButton",
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Delete Task",
            command=self.delete_archived_task,
            style="Danger.TButton",
        ).pack(side=tk.LEFT, padx=5)

    def delete_active_task(self):
        selected_index = self.active_task_list.get_selected_task_index()
        if selected_index >= 0:
            tasks = self.task_manager.storage.get_pending_tasks()
            if 0 <= selected_index < len(tasks):
                task = tasks[selected_index]
                if messagebox.askyesno(
                    "Confirm Delete",
                    "Are you sure you want to delete this task?",
                ):
                    self.task_manager.storage.delete_task(task)
                    self.update_task_lists()

    def delete_archived_task(self):
        selected_index = self.archive_task_list.get_selected_task_index()
        if selected_index >= 0:
            tasks = self.task_manager.storage.get_completed_tasks()
            if 0 <= selected_index < len(tasks):
                task = tasks[selected_index]
                if messagebox.askyesno(
                    "Confirm Delete",
                    "Are you sure you want to delete this task permanently?",
                ):
                    self.task_manager.storage.delete_task(task)
                    self.update_task_lists()

    def on_task_submit(self, task):
        if task not in self.task_manager.storage.tasks:
            if self.task_manager.storage.task_exists(task.title):
                messagebox.showerror("Error", "A task with this title already exists!")
                return
            self.task_manager.storage.add_task(task)
            self.task_manager.storage.save_tasks()
            self.update_task_lists()
        else:
            self.task_manager.storage.save_tasks()
            self.update_task_lists()

    def on_task_delete(self, task):
        if task in self.task_manager.storage.tasks:
            self.task_manager.storage.delete_task(task)
            self.task_manager.storage.save_tasks()
            self.update_task_lists()

    def delete_selected_task(self):
        selected_index = self.active_task_list.get_selected_task_index()
        if selected_index >= 0:
            tasks = self.task_manager.storage.get_pending_tasks()
            if 0 <= selected_index < len(tasks):
                task = tasks[selected_index]
                if messagebox.askyesno(
                    "Confirm Delete", "Are you sure you want to delete this task?"
                ):
                    self.on_task_delete(task)

    def update_task_lists(self):
        active_tasks = self.task_manager.storage.get_pending_tasks()
        self.active_task_list.update_tasks(active_tasks)

        archived_tasks = self.task_manager.storage.get_completed_tasks()
        self.archive_task_list.update_tasks(archived_tasks)

    def refresh_lists(self):
        self.task_manager.storage.load_tasks()
        self.update_task_lists()

    def mark_selected_complete(self):
        selected_index = self.active_task_list.get_selected_task_index()
        if selected_index >= 0:
            tasks = self.task_manager.storage.get_pending_tasks()
            if 0 <= selected_index < len(tasks):
                task = tasks[selected_index]
                task.mark_complete()
                self.task_manager.storage.save_tasks()
                self.update_task_lists()

    def restore_selected_task(self):
        selected_index = self.archive_task_list.get_selected_task_index()
        if selected_index >= 0:
            tasks = self.task_manager.storage.get_completed_tasks()
            if 0 <= selected_index < len(tasks):
                task = tasks[selected_index]
                task.completed = False
                self.task_manager.storage.save_tasks()
                self.update_task_lists()

    def edit_selected_task(self):
        selected_index = self.active_task_list.get_selected_task_index()
        if selected_index >= 0:
            tasks = self.task_manager.storage.get_pending_tasks()
            if 0 <= selected_index < len(tasks):
                task = tasks[selected_index]
                self.task_form.set_edit_mode(task)

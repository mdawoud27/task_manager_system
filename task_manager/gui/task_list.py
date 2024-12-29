"""TaskList component for displaying tasks in a treeview"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .constants import TASK_COLUMNS, STYLE_TAGS


class TaskList(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Create Treeview
        self.create_treeview()

        # Add scrollbar
        self.create_scrollbar()

        # Pack widgets
        self.pack_widgets()

    def create_treeview(self):
        # Create Treeview with columns
        self.tree = ttk.Treeview(
            self, columns=tuple(TASK_COLUMNS.keys()), show="headings", style="Treeview"
        )

        # Configure columns
        for col, width in TASK_COLUMNS.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, minwidth=50)

        # Configure style tags
        for tag, style in STYLE_TAGS.items():
            self.tree.tag_configure(tag, **style)

    def create_scrollbar(self):
        self.scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def pack_widgets(self):
        # Pack with padding for better spacing
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

    def update_tasks(self, tasks):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add tasks to treeview
        for i, task in enumerate(tasks):
            self._insert_task(task, i)

    def _insert_task(self, task, index):
        # Prepare task data
        status = "✓" if task.completed else "○"
        date_str, time_str = self._format_datetime(task.due_date)

        # Prepare row tags
        tags = self._get_row_tags(task, index)

        # Insert task
        self.tree.insert(
            "",
            tk.END,
            values=(status, task.title, task.priority, date_str, time_str),
            tags=tags,
        )

    def _format_datetime(self, due_date):
        if isinstance(due_date, datetime):
            return due_date.strftime("%Y-%m-%d"), due_date.strftime("%H:%M")
        return "-", "-"

    def _get_row_tags(self, task, index):
        tags = []
        if index % 2:
            tags.append("oddrow")
        if task.completed:
            tags.append("completed")
        # Add priority-specific tag
        tags.append(f"{task.priority.lower()}_priority")
        return tags

    def get_selected_task_index(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.index(selection[0])
        return -1

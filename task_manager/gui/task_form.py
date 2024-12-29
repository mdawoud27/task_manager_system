import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ..models import Task


class TaskForm(ttk.Frame):
    def __init__(self, parent, on_submit):
        super().__init__(parent)
        self.on_submit = on_submit
        self.editing_task = None
        self.setup_ui()

    def setup_ui(self):
        # Create a grid with consistent column widths
        self.grid_columnconfigure(1, weight=1)

        # Title
        ttk.Label(self, text="Title:", width=15).grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(
            row=0, column=1, columnspan=3, padx=5, pady=5, sticky="ew"
        )

        # Description
        ttk.Label(self, text="Description:", width=15).grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.desc_text = tk.Text(self, height=3)
        self.desc_text.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Due Date
        ttk.Label(self, text="Due Date:", width=15).grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        self.date_entry = ttk.Entry(self, width=12)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Due Time
        ttk.Label(self, text="Time:", width=8).grid(
            row=2, column=2, padx=5, pady=5, sticky="e"
        )
        self.time_entry = ttk.Entry(self, width=10)
        self.time_entry.insert(0, "HH:MM")
        self.time_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        # Priority
        ttk.Label(self, text="Priority:", width=15).grid(
            row=3, column=0, padx=5, pady=5, sticky="e"
        )
        self.priority_var = tk.StringVar(value="medium")
        priorities = ["low", "medium", "high"]
        self.priority_combo = ttk.Combobox(
            self, textvariable=self.priority_var, values=priorities, state="readonly"
        )
        self.priority_combo.grid(
            row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w"
        )

        # Button Frame
        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)

        # Submit Button
        self.submit_btn = ttk.Button(
            button_frame,
            text="Add Task",
            command=self.submit_task,
            style="Success.TButton",
        )
        self.submit_btn.pack(side=tk.LEFT, padx=5)

        # Cancel Button (hidden by default)
        self.cancel_btn = ttk.Button(
            button_frame, text="Cancel", command=self.cancel_edit
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        self.cancel_btn.pack_forget()

        # Delete Button (hidden by default)
        self.delete_btn = ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_task,
            style="Danger.TButton",
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        self.delete_btn.pack_forget()

    def submit_task(self):
        # Validate title
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Task title cannot be empty!")
            return

        # Get description
        description = self.desc_text.get("1.0", tk.END).strip()

        # Parse due date
        due_date = None
        due_date_str = self.date_entry.get().strip()
        time_str = self.time_entry.get().strip()

        if due_date_str and due_date_str != "YYYY-MM-DD":
            try:
                if time_str and time_str != "HH:MM":
                    due_date = datetime.strptime(
                        f"{due_date_str} {time_str}", "%Y-%m-%d %H:%M"
                    )
                else:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date or time format!")
                return

        # Get priority
        priority = self.priority_var.get()

        # Create or update task
        if self.editing_task:
            self.editing_task.title = title
            self.editing_task.description = description
            self.editing_task.due_date = due_date
            self.editing_task.priority = priority
            task = self.editing_task
        else:
            task = Task(title, description, due_date, priority)

        # Call the callback function
        self.on_submit(task)

        # Clear the form
        self.clear_form()

    def set_edit_mode(self, task):
        self.editing_task = task
        self.submit_btn.configure(text="Update Task")
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        # Fill form with task data
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, task.title)

        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", task.description)

        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

        if task.due_date:
            self.date_entry.insert(0, task.due_date.strftime("%Y-%m-%d"))
            self.time_entry.insert(0, task.due_date.strftime("%H:%M"))
        else:
            self.date_entry.insert(0, "YYYY-MM-DD")
            self.time_entry.insert(0, "HH:MM")

        self.priority_var.set(task.priority)

    def cancel_edit(self):
        self.editing_task = None
        self.submit_btn.configure(text="Add Task")
        self.cancel_btn.pack_forget()
        self.delete_btn.pack_forget()
        self.clear_form()

    def delete_task(self):
        if self.editing_task and messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this task?"
        ):
            self.on_delete(self.editing_task)
            self.clear_form()

    def clear_form(self):
        self.editing_task = None
        self.submit_btn.configure(text="Add Task")
        self.cancel_btn.pack_forget()
        self.delete_btn.pack_forget()

        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "HH:MM")
        self.priority_var.set("medium")

from task_manager.gui.main_window import MainWindow
from task_manager.main import TaskManager

if __name__ == "__main__":
    task_manager = TaskManager()
    app = MainWindow(task_manager)
    app.mainloop()

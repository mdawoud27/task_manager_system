# Task Manager

A task management application with both **GUI** and **CLI** interfaces, built with **Python**. Manage tasks efficiently with features like _priority-based sorting_, _task archiving_, and more.

## Features

- **Dual Interface**: Choose between **_GUI_** or **_CLI_** based on your preference
- **Task Management**: you can do **_CRUD_** operations on the tasks
- **Task Organization**:
  - Priority-based sorting (_High_, _Medium_, _Low_)
  - Separate views for active and archived tasks
  - Automatic task sorting based on priority
- **Data Persistence**: All tasks are automatically saved to a `JSON` file
- **Input Validation**: Prevents _duplicate_ task titles and invalid dates
- **User-Friendly Interface**:

  - Clean and intuitive GUI
  - Easy-to-use form controls
  - Confirmation dialogs for important actions
  - Visual indicators for task status and priority

- **Archive System**:
  - Completed tasks moved to archive
  - Can be restored or permanently deleted
  - Keeps active tasks list clean

## Project Structure

```bash
task_manager_system
├── main.py                # The entry point to GUI interface
├── README.md
├── task_manager
│   ├── cli                # CLI Configurations
│   │   ├── commands.py
│   │   ├── __init__.py
│   │   └── interface.py
│   ├── gui                # GUI Configurations
│   │   ├── constants.py   # GUI-related constants and configurations
│   │   ├── __init__.py
│   │   ├── main_window.py # Main application window
│   │   ├── styles.py      # GUI styling definitions
│   │   ├── task_form.py   # Task creation/editing form
│   │   └── task_list.py   # Task list display component
│   ├── __init__.py
│   ├── main.py            # The entry point to CLI interface
│   ├── models.py          # Task data model
│   └── storage.py         # Data persistence handling
└── tasks.json
```

## Installation

1. Clone the Repo:

   ```bash
   git clone https://github.com/mdawoud27/task_manager_system.git
   cd task_manager_system
   ```

2. Run the application:

   ```bash
   # For GUI interface
   python3 main.py

   # For CLI interface
   python3 -m task_manager.main
   ```

## Future Enhancements

- Task categories/tags
- Task search functionality
- Due date reminders
- Multiple task lists
- Data export/import
- Task priorities customization
- Dark/Light theme support
- Storage the data in database not `json` file
- Anything else ...

## Contribution

1. Fork the project
2. Create your feature branch (`git switch -c feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: <short-description>'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

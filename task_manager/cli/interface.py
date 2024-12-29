"""Main CLI interface"""


class CLI:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.commands = None  # Will be initialized in run()

    def display_menu(self):
        """Display the main menu"""
        print("\n=== Task Manager ===")
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. Mark Task as Complete")
        print("6. Exit")
        return input("Choose an option (1-6): ").strip()

    def run(self):
        """Run the CLI interface"""
        from .commands import CLICommands

        self.commands = CLICommands(self.task_manager)

        while True:
            choice = self.display_menu()

            if choice == "1":
                self.commands.add_task()
            elif choice == "2":
                self.commands.view_tasks(
                    self.task_manager.storage.get_all_tasks(), "All Tasks"
                )
            elif choice == "3":
                self.commands.view_tasks(
                    self.task_manager.storage.get_pending_tasks(), "Pending Tasks"
                )
            elif choice == "4":
                self.commands.view_tasks(
                    self.task_manager.storage.get_completed_tasks(), "Completed Tasks"
                )
            elif choice == "5":
                self.commands.mark_task_complete()
            elif choice == "6":
                print("\nThank you for using Task Manager!")
                break
            else:
                print("\nInvalid option. Please try again.")

from datetime import datetime


class Task:
    def __init__(
        self,
        title,
        description,
        due_date=None,
        priority="medium",
        completed=False,
        created_at=None,
    ):
        self.title = title
        self.description = description
        self.created_at = created_at if created_at else datetime.now()

        # Convert string to datetime if needed
        if isinstance(due_date, str):
            try:
                self.due_date = datetime.fromisoformat(due_date)
            except ValueError:
                self.due_date = None
        else:
            self.due_date = due_date

        self.priority = priority
        self.completed = completed

    def to_dict(self):
        """Convert task to dictionary for JSON serialization"""
        return {
            "title": self.title,
            "description": self.description,
            "created_at": (
                self.created_at.isoformat()
                if isinstance(self.created_at, datetime)
                else self.created_at
            ),
            "due_date": (
                self.due_date.isoformat()
                if isinstance(self.due_date, datetime)
                else self.due_date
            ),
            "priority": self.priority,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary"""
        # Convert ISO format strings to datetime objects
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("due_date"), str):
            data["due_date"] = datetime.fromisoformat(data["due_date"])
        return cls(**data)

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "✗"
        due = f", Due: {self.due_date}" if self.due_date else ""
        return f"[{status}] {self.title} ({self.priority}{due})\n  {self.description}"

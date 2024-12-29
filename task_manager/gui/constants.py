"""Constants used across the GUI components"""

# TreeView Columns
TASK_COLUMNS = {
    "Status": 80,
    "Title": 300,
    "Priority": 120,
    "Due Date": 120,
    "Due Time": 120,
}

# Priority Colors
PRIORITY_COLORS = {"low": "#5a9cfc", "medium": "#fead3b", "high": "#e4435b"}

# Style Tags
STYLE_TAGS = {
    "completed": {"foreground": "gray"},
    "low_priority": {"foreground": PRIORITY_COLORS["low"]},
    "medium_priority": {"foreground": PRIORITY_COLORS["medium"]},
    "high_priority": {"foreground": PRIORITY_COLORS["high"]},
    "oddrow": {"background": "#F5F5F5"},
}

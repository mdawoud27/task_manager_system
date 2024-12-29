from tkinter import ttk


def configure_styles():
    style = ttk.Style()

    # Configure Treeview styles
    style.configure("Treeview", rowheight=50, padding=5)
    style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), padding=10)

    # Configure other common styles
    style.configure("TaskFrame.TFrame", padding=5)
    style.configure("Header.TLabel", font=("Helvetica", 12, "bold"), padding=5)

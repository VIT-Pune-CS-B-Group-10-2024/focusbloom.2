import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

SAGE_GREEN = "#c1d9c0"
BABY_PINK = "#f9e6e7"
SKY_BLUE = "#d6e7f5"
WHITE = "#ffffff"
DARK_TEXT = "#3a3a3a"

class TodoFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        add_frame = ttk.Frame(self, style="TFrame")
        add_frame.pack(pady=20)
        self.task_entry = ttk.Entry(add_frame, font=("Segoe UI", 13), width=30)
        self.task_entry.pack(side=tk.LEFT, padx=8, ipady=6)
        self.priority_var = tk.StringVar()
        self.priority_combobox = ttk.Combobox(add_frame, textvariable=self.priority_var,
                                              values=["High", "Medium", "Low"], state="readonly", font=("Segoe UI", 12), width=8)
        self.priority_combobox.current(1)
        self.priority_combobox.pack(side=tk.LEFT, padx=8, ipady=3)
        ttk.Button(add_frame, text="Add Task", command=self.add_task, style="TButton").pack(side=tk.LEFT, padx=8, ipadx=8, ipady=3)

        self.tree = ttk.Treeview(self, columns=("Priority", "Status"), show="headings", height=10)
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.column("Priority", width=100, anchor='center')
        self.tree.column("Status", width=100, anchor='center')
        self.tree.pack(fill="both", expand=True, padx=30, pady=15)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        btn_frame = ttk.Frame(self, style="TFrame")
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Mark Complete", command=self.mark_complete, style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        ttk.Button(btn_frame, text="Delete Task", command=self.delete_task, style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        ttk.Button(btn_frame, text="Back", command=lambda: self.controller.show_frame("WelcomeFrame"), style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task")
            return
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO todos (user_id, task, priority) VALUES (?, ?, ?)",
                 (self.controller.current_user, task, priority))
        conn.commit()
        conn.close()
        self.task_entry.delete(0, tk.END)
        self.load_tasks()

    def load_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT id, task, priority, completed FROM todos WHERE user_id=?",
                 (self.controller.current_user,))
        total = 0
        completed = 0
        for task in c.fetchall():
            status = "Complete" if task[3] else "Pending"
            self.tree.insert("", "end", iid=task[0], values=(task[2], status), text=task[1])
            total += 1
            if task[3]:
                completed += 1
        conn.close()
        self.progress["value"] = (completed / total) * 100 if total > 0 else 0

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = selected[0]
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("UPDATE todos SET completed=1 WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        self.load_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = selected[0]
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("DELETE FROM todos WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        self.load_tasks()

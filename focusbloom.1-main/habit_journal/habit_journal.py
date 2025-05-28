import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date

SAGE_GREEN = "#c1d9c0"
BABY_PINK = "#f9e6e7"
SKY_BLUE = "#d6e7f5"
WHITE = "#ffffff"
DARK_TEXT = "#3a3a3a"

class HabitJournalFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        self.create_widgets()
        self.load_habits()
        self.load_journal()
        self.update_streak()

    def create_widgets(self):
        habit_frame = ttk.Labelframe(self, text="Daily Habit Log", style="TLabelframe")
        habit_frame.pack(fill="x", padx=30, pady=15)
        self.habit_entry = ttk.Entry(habit_frame, font=("Segoe UI", 13), width=25)
        self.habit_entry.pack(side=tk.LEFT, padx=8, ipady=6)
        ttk.Button(habit_frame, text="Log Habit", command=self.log_habit, style="TButton").pack(side=tk.LEFT, padx=8, ipadx=8, ipady=5)
        self.habit_list = tk.Listbox(habit_frame, height=3, font=("Segoe UI", 12), bg=SKY_BLUE, fg=DARK_TEXT)
        self.habit_list.pack(side=tk.LEFT, padx=8, pady=5)

        self.streak_label = ttk.Label(self, text="Current Streak: 0 days", style="TLabel", font=("Segoe UI", 13, "bold"))
        self.streak_label.pack(pady=8)

        journal_frame = ttk.Labelframe(self, text="Journal Entry", style="TLabelframe")
        journal_frame.pack(fill="x", padx=30, pady=10)
        self.journal_text = tk.Text(journal_frame, height=4, width=50, font=("Segoe UI", 12), bg=BABY_PINK, fg=DARK_TEXT)
        self.journal_text.pack(side=tk.LEFT, padx=8, pady=8)
        ttk.Button(journal_frame, text="Save Entry", command=self.save_journal, style="TButton").pack(side=tk.LEFT, padx=8, ipadx=8, ipady=5)

        self.journal_history = tk.Listbox(self, height=6, font=("Segoe UI", 12), bg=SKY_BLUE, fg=DARK_TEXT)
        self.journal_history.pack(fill="both", padx=30, pady=15, expand=True)

        ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("WelcomeFrame"), style="TButton").pack(pady=10, ipadx=10, ipady=5)

    def log_habit(self):
        habit = self.habit_entry.get()
        if not habit:
            messagebox.showwarning("Warning", "Enter a habit")
            return
        today = date.today().isoformat()
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO habits (user_id, habit, date, status) VALUES (?, ?, ?, ?)",
                  (self.controller.current_user, habit, today, 1))
        conn.commit()
        conn.close()
        self.habit_entry.delete(0, tk.END)
        self.load_habits()
        self.update_streak()

    def load_habits(self):
        self.habit_list.delete(0, tk.END)
        today = date.today().isoformat()
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT habit FROM habits WHERE user_id=? AND date=? AND status=1",
                  (self.controller.current_user, today))
        for row in c.fetchall():
            self.habit_list.insert(tk.END, row[0])
        conn.close()

    def save_journal(self):
        entry = self.journal_text.get("1.0", tk.END).strip()
        if not entry:
            messagebox.showwarning("Warning", "Journal entry cannot be empty")
            return
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO journal (user_id, entry) VALUES (?, ?)",
                  (self.controller.current_user, entry))
        conn.commit()
        conn.close()
        self.journal_text.delete("1.0", tk.END)
        self.load_journal()

    def load_journal(self):
        self.journal_history.delete(0, tk.END)
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT entry, created_at FROM journal WHERE user_id=? ORDER BY created_at DESC LIMIT 10",
                  (self.controller.current_user,))
        for row in c.fetchall():
            self.journal_history.insert(tk.END, f"{row[1][:10]}: {row[0]}")
        conn.close()

    def update_streak(self):
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT date FROM habits WHERE user_id=? AND status=1 ORDER BY date DESC",
                  (self.controller.current_user,))
        dates = [row[0] for row in c.fetchall()]
        streak = 0
        today = date.today()
        for i, d in enumerate(dates):
            if (today - datetime.strptime(d, "%Y-%m-%d").date()).days == i:
                streak += 1
            else:
                break
        self.streak_label.config(text=f"Current Streak: {streak} days")
        conn.close()

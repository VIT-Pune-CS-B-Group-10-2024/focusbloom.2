import tkinter as tk
import datetime
from tkinter import ttk, messagebox
import sqlite3
from datetime import date
from tkcalendar import Calendar

SAGE_GREEN = "#c1d9c0"
BABY_PINK = "#f9e6e7"
SKY_BLUE = "#d6e7f5"
WHITE = "#ffffff"
DARK_TEXT = "#3a3a3a"

class MoodReminderFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        self.create_widgets()
        self.load_moods()

    def create_widgets(self):
        mood_frame = ttk.Labelframe(self, text="Daily Mood Log", style="TLabelframe")
        mood_frame.pack(fill="x", padx=30, pady=15)
        ttk.Label(mood_frame, text="Mood (1-5):", style="TLabel").pack(side=tk.LEFT, padx=8)
        self.mood_var = tk.IntVar(value=3)
        ttk.Spinbox(mood_frame, from_=1, to=5, textvariable=self.mood_var, width=5, font=("Segoe UI", 13)).pack(side=tk.LEFT, padx=8)
        self.notes_entry = ttk.Entry(mood_frame, width=30, font=("Segoe UI", 13))
        self.notes_entry.pack(side=tk.LEFT, padx=8, ipady=6)
        ttk.Button(mood_frame, text="Log Mood", command=self.log_mood, style="TButton").pack(side=tk.LEFT, padx=8, ipadx=8, ipady=5)

        cal_frame = ttk.Labelframe(self, text="Mood Calendar", style="TLabelframe")
        cal_frame.pack(fill="x", padx=30, pady=10)
        self.calendar = Calendar(cal_frame, selectmode='day', background=SKY_BLUE, foreground=DARK_TEXT, headersbackground=SAGE_GREEN)
        self.calendar.pack(pady=8)
        ttk.Button(cal_frame, text="Show Mood", command=self.show_mood_on_calendar, style="TButton").pack(pady=8, ipadx=8, ipady=5)
        self.mood_label = ttk.Label(cal_frame, text="", style="TLabel", font=("Segoe UI", 13, "bold"), foreground=BABY_PINK)
        self.mood_label.pack()

        reminder_frame = ttk.Labelframe(self, text="Reminders", style="TLabelframe")
        reminder_frame.pack(fill="x", padx=30, pady=10)
        ttk.Button(reminder_frame, text="Set Break Reminder", command=self.set_reminder, style="TButton").pack(pady=8, ipadx=8, ipady=5)

        ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("WelcomeFrame"), style="TButton").pack(pady=15, ipadx=10, ipady=5)

    def log_mood(self):
        score = self.mood_var.get()
        notes = self.notes_entry.get()
        today = date.today().isoformat()
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO mood (user_id, score, notes, created_at) VALUES (?, ?, ?, ?)",
                  (self.controller.current_user, score, notes, today))
        conn.commit()
        conn.close()
        self.notes_entry.delete(0, tk.END)
        self.load_moods()
        messagebox.showinfo("Mood", "Mood logged!")

    def load_moods(self):
        self.mood_data = {}
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT created_at, score FROM mood WHERE user_id=?", (self.controller.current_user,))
        for row in c.fetchall():
            self.mood_data[row[0]] = row[1]
        conn.close()

    def show_mood_on_calendar(self):
        sel_date = self.calendar.get_date()
# Convert calendar date (e.g., '05/29/2025') to '2025-05-29'
        try:
            date_obj = datetime.datetime.strptime(sel_date, "%m/%d/%y")
        except ValueError:
            date_obj = datetime.datetime.strptime(sel_date, "%m/%d/%Y")
        sel_date_db = date_obj.strftime("%Y-%m-%d")
        mood = self.mood_data.get(sel_date_db, "No entry")
        self.mood_label.config(text=f"Mood on {sel_date}: {mood}")

    def set_reminder(self):
        messagebox.showinfo("Reminder", "Don't forget to take a break and check in with yourself!")

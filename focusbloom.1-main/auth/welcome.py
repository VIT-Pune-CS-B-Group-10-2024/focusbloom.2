import tkinter as tk
from tkinter import ttk
import random
import sqlite3

SAGE_GREEN = "#c1d9c0"
BABY_PINK = "#f9e6e7"
WHITE = "#ffffff"
DARK_TEXT = "#3a3a3a"

class WelcomeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        self.quote = random.choice([
            "You are capable of amazing things",
            "Progress, not perfection",
            "Small steps lead to big changes",
            "Your mental health matters"
        ])
        self.create_widgets()

    def create_widgets(self):
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE id=?", (self.controller.current_user,))
        username = c.fetchone()[0]
        conn.close()

        ttk.Label(self, text=f"Welcome, {username}!", style="TLabel", font=("Segoe UI", 18, "bold")).pack(pady=15)
        ttk.Label(self, text=self.quote, style="TLabel", wraplength=500, font=("Segoe UI", 14), foreground=SAGE_GREEN).pack(pady=10)

        nav_frame = ttk.Frame(self, style="TFrame")
        nav_frame.pack(pady=20)

        buttons = [
            ("To-Do List", "TodoFrame"),
            ("Habit Tracker", "HabitJournalFrame"),
            ("Productivity Tools", "ProductivityFrame"),
            ("Mood Tracker", "MoodReminderFrame"),
            ("Music & Meditation", "MusicMotivationFrame")
        ]

        for text, frame in buttons:
            btn = ttk.Button(nav_frame, text=text, style="TButton",
                             command=lambda f=frame: self.controller.show_frame(f))
            btn.pack(pady=8, ipadx=15, ipady=8, fill='x')

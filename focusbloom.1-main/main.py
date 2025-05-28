import tkinter as tk
from tkinter import ttk
from auth.auth import AuthFrame
from auth.welcome import WelcomeFrame
from todo.todo import TodoFrame
from habit_journal.habit_journal import HabitJournalFrame
from productivity.productivity import ProductivityFrame
from mood_reminder.mood_reminder import MoodReminderFrame
from music_motivation.music_motivation import MusicMotivationFrame
from db import init_db

# Calming color palette
SAGE_GREEN = "#c1d9c0"
BABY_PINK = "#f9e6e7"
SKY_BLUE = "#d6e7f5"
WHITE = "#ffffff"
DARK_TEXT = "#3a3a3a"

class MentalHealthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mental Health App")
        self.geometry("1000x700")
        self.current_user = None

        self.configure(bg=WHITE)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=WHITE)
        style.configure("TLabel", background=WHITE, foreground=DARK_TEXT, font=("Segoe UI", 13))
        style.configure("TButton", background=SAGE_GREEN, foreground=DARK_TEXT, font=("Segoe UI", 12, "bold"), padding=8)
        style.map("TButton",
                  background=[("active", SKY_BLUE), ("!active", SAGE_GREEN)],
                  foreground=[("active", DARK_TEXT), ("!active", DARK_TEXT)])
        style.configure("TLabelframe", background=WHITE, foreground=SAGE_GREEN, font=("Segoe UI", 14, "bold"))
        style.configure("TLabelframe.Label", background=WHITE, foreground=SAGE_GREEN, font=("Segoe UI", 14, "bold"))
        style.configure("Treeview", background=WHITE, fieldbackground=WHITE, foreground=DARK_TEXT, font=("Segoe UI", 12))
        style.configure("TEntry", fieldbackground=BABY_PINK, background=BABY_PINK, font=("Segoe UI", 12))

        self.container = tk.Frame(self, bg=WHITE)
        self.container.pack(fill="both", expand=True)

        self.show_frame("AuthFrame")

    def show_frame(self, frame_name):
        for widget in self.container.winfo_children():
            widget.destroy()

        frames = {
            "AuthFrame": AuthFrame,
            "WelcomeFrame": WelcomeFrame,
            "TodoFrame": TodoFrame,
            "HabitJournalFrame": HabitJournalFrame,
            "ProductivityFrame": ProductivityFrame,
            "MoodReminderFrame": MoodReminderFrame,
            "MusicMotivationFrame": MusicMotivationFrame
        }
        frame_class = frames[frame_name]
        frame = frame_class(self.container, self)
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    init_db()
    app = MentalHealthApp()
    app.mainloop()

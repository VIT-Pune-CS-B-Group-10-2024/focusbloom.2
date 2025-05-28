import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sqlite3
from datetime import date

SAGE_GREEN = "#c1d9c0"
BABY_PINK = "#f9e6e7"
SKY_BLUE = "#d6e7f5"
WHITE = "#ffffff"
DARK_TEXT = "#3a3a3a"

class ProductivityFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pomodoro_time = 25 * 60
        self.break_time = 5 * 60
        self.time_left = self.pomodoro_time
        self.is_running = False
        self.is_break = False
        self.pomodoro_count = 0
        self.screen_time = 0
        self.configure(style="TFrame")
        self.create_widgets()

    def create_widgets(self):
        # Pomodoro Timer
        pomodoro_frame = ttk.Labelframe(self, text="Pomodoro Timer", style="TLabelframe")
        pomodoro_frame.pack(fill="x", padx=30, pady=15)
        self.timer_label = ttk.Label(pomodoro_frame, text=self.format_time(self.time_left), font=("Segoe UI", 32, "bold"), foreground=SKY_BLUE)
        self.timer_label.pack(pady=10)
        btn_frame = ttk.Frame(pomodoro_frame, style="TFrame")
        btn_frame.pack()
        ttk.Button(btn_frame, text="Start", command=self.start_timer, style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        ttk.Button(btn_frame, text="Pause", command=self.pause_timer, style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset_timer, style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        self.pomodoro_label = ttk.Label(pomodoro_frame, text="Pomodoros Completed: 0", font=("Segoe UI", 14, "bold"), foreground=SAGE_GREEN)
        self.pomodoro_label.pack(pady=8)

        # Screen Time Tracker
        screen_frame = ttk.Labelframe(self, text="Screen Time Tracker", style="TLabelframe")
        screen_frame.pack(fill="x", padx=30, pady=10)
        self.screen_label = ttk.Label(screen_frame, text="Screen Time: 0 min", font=("Segoe UI", 13), foreground=BABY_PINK)
        self.screen_label.pack(pady=8)
        ttk.Button(screen_frame, text="Start Tracking", command=self.start_screen_tracking, style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        ttk.Button(screen_frame, text="Stop Tracking", command=self.stop_screen_tracking, style="TButton").pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        # Procrastination Tracker
        procrast_frame = ttk.Labelframe(self, text="Procrastination Tracker", style="TLabelframe")
        procrast_frame.pack(fill="x", padx=30, pady=10)
        ttk.Button(procrast_frame, text="Show Tasks Done vs Planned", command=self.show_procrastination, style="TButton").pack(pady=8, ipadx=10, ipady=5)
        self.procrast_label = ttk.Label(procrast_frame, text="", font=("Segoe UI", 13, "bold"), foreground=SKY_BLUE)
        self.procrast_label.pack(pady=8)

        ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("WelcomeFrame"), style="TButton").pack(pady=15, ipadx=10, ipady=5)

    def format_time(self, seconds):
        return f"{seconds // 60:02}:{seconds % 60:02}"

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.run_timer()

    def run_timer(self):
        if self.is_running and self.time_left > 0:
            self.timer_label.config(text=self.format_time(self.time_left))
            self.time_left -= 1
            self.after(1000, self.run_timer)
        elif self.time_left == 0:
            if not self.is_break:
                self.pomodoro_count += 1
                self.save_pomodoro()
                messagebox.showinfo("Pomodoro", "Work session complete! Take a break.")
                self.time_left = self.break_time
                self.is_break = True
                self.timer_label.config(text=self.format_time(self.time_left))
                self.run_timer()
            else:
                messagebox.showinfo("Break", "Break over! Start another pomodoro.")
                self.time_left = self.pomodoro_time
                self.is_break = False
                self.timer_label.config(text=self.format_time(self.time_left))
                self.is_running = False
            self.pomodoro_label.config(text=f"Pomodoros Completed: {self.pomodoro_count}")

    def pause_timer(self):
        self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.is_break = False
        self.time_left = self.pomodoro_time
        self.timer_label.config(text=self.format_time(self.time_left))

    def save_pomodoro(self):
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        today = date.today().isoformat()
        c.execute("SELECT id, pomodoro_count FROM productivity WHERE user_id=? AND date=?",
                  (self.controller.current_user, today))
        row = c.fetchone()
        if row:
            c.execute("UPDATE productivity SET pomodoro_count=? WHERE id=?",
                      (self.pomodoro_count, row[0]))
        else:
            c.execute("INSERT INTO productivity (user_id, pomodoro_count, screen_time, date) VALUES (?, ?, ?, ?)",
                      (self.controller.current_user, self.pomodoro_count, self.screen_time, today))
        conn.commit()
        conn.close()

    # --- Screen Time Tracking ---
    def start_screen_tracking(self):
        self.screen_time = 0
        self.screen_tracking = True
        self.screen_thread = threading.Thread(target=self.track_screen_time)
        self.screen_thread.daemon = True
        self.screen_thread.start()

    def stop_screen_tracking(self):
        self.screen_tracking = False
        self.save_screen_time()

    def track_screen_time(self):
        while getattr(self, 'screen_tracking', False):
            time.sleep(60)
            self.screen_time += 1
            self.screen_label.config(text=f"Screen Time: {self.screen_time} min")

    def save_screen_time(self):
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        today = date.today().isoformat()
        c.execute("SELECT id, screen_time FROM productivity WHERE user_id=? AND date=?",
                  (self.controller.current_user, today))
        row = c.fetchone()
        if row:
            c.execute("UPDATE productivity SET screen_time=? WHERE id=?",
                      (self.screen_time, row[0]))
        else:
            c.execute("INSERT INTO productivity (user_id, pomodoro_count, screen_time, date) VALUES (?, ?, ?, ?)",
                      (self.controller.current_user, self.pomodoro_count, self.screen_time, today))
        conn.commit()
        conn.close()

    # --- Procrastination Tracker ---
    def show_procrastination(self):
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM todos WHERE user_id=?",
                  (self.controller.current_user,))
        planned = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM todos WHERE user_id=? AND completed=1",
                  (self.controller.current_user,))
        done = c.fetchone()[0]
        conn.close()
        self.procrast_label.config(text=f"Planned: {planned} | Done: {done} | Procrastination: {planned - done}")

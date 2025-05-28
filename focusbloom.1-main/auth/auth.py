import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

SAGE_GREEN = "#c1d9c0"
BABY_PINK = "#f9e6e7"
WHITE = "#ffffff"
DARK_TEXT = "#3a3a3a"

class AuthFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        ttk.Label(self, text="Username:", style="TLabel").grid(row=0, column=0, padx=20, pady=15, sticky="e")
        self.username_entry = ttk.Entry(self, font=("Segoe UI", 14))
        self.username_entry.grid(row=0, column=1, padx=20, pady=15, sticky="w")

        ttk.Label(self, text="Password:", style="TLabel").grid(row=1, column=0, padx=20, pady=15, sticky="e")
        self.password_entry = ttk.Entry(self, show="*", font=("Segoe UI", 14))
        self.password_entry.grid(row=1, column=1, padx=20, pady=15, sticky="w")

        btn_frame = ttk.Frame(self, style="TFrame")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        login_btn = ttk.Button(btn_frame, text="Login", command=self.login, style="TButton")
        login_btn.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        signup_btn = ttk.Button(btn_frame, text="Sign Up", command=self.signup, style="TButton")
        signup_btn.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            self.controller.current_user = user[0]
            self.controller.show_frame("WelcomeFrame")
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "All fields required")
            return
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created! Please login")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

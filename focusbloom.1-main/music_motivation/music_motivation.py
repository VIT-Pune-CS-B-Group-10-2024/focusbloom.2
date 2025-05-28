import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import os
import random

SAGE_GREEN = "#c1d9c0"
BABY_PINK = "#f9e6e7"
SKY_BLUE = "#d6e7f5"
WHITE = "#ffffff"
DARK_TEXT = "#3a3a3a"

class MusicMotivationFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        pygame.mixer.init()
        self.configure(style="TFrame")
        self.create_widgets()

    def create_widgets(self):
        # Music Player
        music_frame = ttk.Labelframe(self, text="Ambient Music Player", style="TLabelframe")
        music_frame.pack(fill="x", padx=30, pady=15)
        self.music_files = self.get_music_files()
        self.music_list = tk.Listbox(music_frame, height=3, font=("Segoe UI", 12), bg=SKY_BLUE, fg=DARK_TEXT)
        for f in self.music_files:
            self.music_list.insert(tk.END, f)
        self.music_list.pack(side=tk.LEFT, padx=8, pady=8)
        ttk.Button(music_frame, text="Play", command=self.play_music, style="TButton").pack(side=tk.LEFT, padx=8, ipadx=8, ipady=5)
        ttk.Button(music_frame, text="Stop", command=self.stop_music, style="TButton").pack(side=tk.LEFT, padx=8, ipadx=8, ipady=5)

        # Guided Meditation
        meditation_frame = ttk.Labelframe(self, text="Guided Meditation", style="TLabelframe")
        meditation_frame.pack(fill="x", padx=30, pady=10)
        self.meditation_files = self.get_meditation_files()
        self.meditation_list = tk.Listbox(meditation_frame, height=3, font=("Segoe UI", 12), bg=BABY_PINK, fg=DARK_TEXT)
        for f in self.meditation_files:
            self.meditation_list.insert(tk.END, f)
        self.meditation_list.pack(side=tk.LEFT, padx=8, pady=8)
        ttk.Button(meditation_frame, text="Play", command=self.play_meditation, style="TButton").pack(side=tk.LEFT, padx=8, ipadx=8, ipady=5)
        ttk.Button(meditation_frame, text="Stop", command=self.stop_music, style="TButton").pack(side=tk.LEFT, padx=8, ipadx=8, ipady=5)

        # Motivational Quotes
        quote_frame = ttk.Labelframe(self, text="Motivational Quotes", style="TLabelframe")
        quote_frame.pack(fill="x", padx=30, pady=10)
        self.quote_label = ttk.Label(quote_frame, text=self.get_random_quote(), wraplength=500, font=("Segoe UI", 14), foreground=SAGE_GREEN)
        self.quote_label.pack(pady=10)
        ttk.Button(quote_frame, text="New Quote", command=self.show_new_quote, style="TButton").pack(pady=8, ipadx=8, ipady=5)

        ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("WelcomeFrame"), style="TButton").pack(pady=15, ipadx=10, ipady=5)

    def get_music_files(self):
        music_dir = os.path.join("assets", "music")
        if not os.path.exists(music_dir):
            os.makedirs(music_dir)
        return [f for f in os.listdir(music_dir) if f.endswith(('.wav', '.ogg'))]

    def get_meditation_files(self):
        meditation_dir = os.path.join("assets", "meditation")
        if not os.path.exists(meditation_dir):
            os.makedirs(meditation_dir)
        return [f for f in os.listdir(meditation_dir) if f.endswith(('.wav', '.ogg'))]

    def play_music(self):
        idx = self.music_list.curselection()
        if not idx:
            messagebox.showinfo("Info", "Please select a music file.")
            return
        file = self.music_files[idx[0]]
        path = os.path.join("assets", "music", file)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def play_meditation(self):
        idx = self.meditation_list.curselection()
        if not idx:
            messagebox.showinfo("Info", "Please select a meditation file.")
            return
        file = self.meditation_files[idx[0]]
        path = os.path.join("assets", "meditation", file)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def get_random_quote(self):
        quotes_path = os.path.join("assets", "quotes.txt")
        if not os.path.exists(quotes_path):
            with open(quotes_path, "w") as f:
                f.write("You are enough.\nKeep going.\nBreathe in, breathe out.\n")
        with open(quotes_path, "r") as f:
            quotes = [line.strip() for line in f if line.strip()]
        return random.choice(quotes) if quotes else "Stay motivated!"

    def show_new_quote(self):
        self.quote_label.config(text=self.get_random_quote())

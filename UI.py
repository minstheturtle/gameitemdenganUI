import tkinter as tk
from tkinter import ttk

class KomponenUI:
    @staticmethod
    def buat_tombol_game(parent, text, bg_color, hover_color, fg_color, command):
        """Membuat tombol ala game interaktif dengan efek hover halus"""
        btn = tk.Button(parent, text=text, bg=bg_color, fg=fg_color,
                        font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                        activebackground=hover_color, activeforeground=fg_color,
                        bd=0, padx=15, pady=8, cursor="hand2", command=command)
        
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        return btn

    @staticmethod
    def buat_panel_game(parent, bg_color="#161b22", border_color="#30363d"):
        """Membuat kotak panel dengan border gaya cyberpunk/RPG"""
        frame = tk.Frame(parent, bg=border_color, padx=1, pady=1)
        inner = tk.Frame(frame, bg=bg_color, padx=15, pady=15)
        inner.pack(fill=tk.BOTH, expand=True)
        return frame, inner
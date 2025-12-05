import tkinter as tk
from tkinter import ttk
import platform

WIDTH = 1000
HEIGHT = 650
TITLE = "Grand Strife Launcher"

COLORS = {
    'bg': '#121212',
    'panel': '#1E1E1E',
    'accent': '#3A7BD5',
    'muted': '#B3B3B3',
    'fg': '#E6E6E6',
    'danger': '#E06363'
}

class mainApp(tk.Tk):
    def __init__(self, width=WIDTH, height=HEIGHT):
        super().__init__()
        self.title(TITLE)
        self.configure(bg=COLORS['bg'])

        if platform.system() == 'Windows':
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass

        self.style = ttk.Style(self)

        defaultFont = ("Segoe UI", 10) if platform.system() == 'Windows' else ("Sans", 10)
        self.option_add("*Font", defaultFont)

        self.style.theme_use('clam')

        self.style.configure('Dark.TFrame', background=COLORS['panel'])
        self.style.configure('Dark.TLabel', background=COLORS['panel'], foreground=COLORS['fg'])
        self.style.configure('Dark.TButton', background=COLORS['panel'], foreground=COLORS['fg'], relief='flat')
        self.style.map('Dark.TButton', background=[('active', COLORS['accent'])])

        self.style.configure('Dark.Treeview',
                             background=COLORS['panel'],
                             fieldbackground=COLORS['panel'],
                             foreground=COLORS['fg'],
                             rowheight=26)
        self.style.map('Dark.Treeview', background=[('selected', COLORS['accent'])], foreground=[('selected', '#ffffff')])

        self.style.configure('Dark.TNotebook', background=COLORS['bg'])
        self.style.configure('Dark.TNotebook.Tab', background=COLORS['panel'], foreground=COLORS['fg'])

if __name__ == '__main__':
    app = mainApp()
    app.mainloop()

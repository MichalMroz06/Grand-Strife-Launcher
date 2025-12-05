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

        self.createWidgets()
    
    def createWidgets(self):
        toolbar = ttk.Frame(self, style='Dark.TFrame')
        toolbar.pack(side='top', fill='x', padx=8, pady=6)

        # Button section
        startBtn = ttk.Button(toolbar, text='Start', style='Dark.TButton', command=self.startGame)
        resumeBtn = ttk.Button(toolbar, text='Resume', style='Dark.TButton', command=self.resumeGame)
        folderBtn = ttk.Button(toolbar, text='Open folder', style='Dark.TButton', command=self.openFolder)

        startBtn.pack(side='left', padx=4)
        resumeBtn.pack(side='left', padx=4)
        folderBtn.pack(side='left', padx=4)

        # Main panel
        mainPanel = ttk.Frame(self, style='Dark.TFrame')
        mainPanel.pack(side='top', fill='both', expand=True, padx=8, pady=(0,8))

        mainPanel.columnconfigure(1, weight=1)
        mainPanel.rowconfigure(0, weight=1)

        # Left panel
        leftPanel = ttk.Frame(mainPanel, style='Dark.TFrame')
        leftPanel.grid(row=0, column=0, sticky='nsw', padx=(0,8))

        leftPanel.config(width=240)

        lblNav = ttk.Label(leftPanel, text='Content', style='Dark.TLabel')
        lblNav.pack(anchor='w', padx=6, pady=(6,2))

        self.tree = ttk.Treeview(leftPanel, style='Dark.Treeview', show='tree')
        self.tree.pack(fill='both', expand=True, padx=6, pady=4)

        # Right panel
        rightPanel = ttk.Frame(mainPanel, style='Dark.TFrame')
        rightPanel.grid(row=0, column=1, sticky='nsew')
        rightPanel.columnconfigure(0, weight=1)
        rightPanel.rowconfigure(0, weight=1)

        notebook = ttk.Notebook(rightPanel, style='Dark.TNotebook')
        notebook.grid(row=0, column=0, sticky='nsew')

        # Info section
        infoFrame = ttk.Frame(notebook, style='Dark.TFrame')
        infoFrame.columnconfigure(0, weight=1)
        infoFrame.rowconfigure(0, weight=1)

        notebook.add(infoFrame, text='Info')
        
        # Text widget
        self.infoText = tk.Text(infoFrame, height=8, bg=COLORS['bg'], fg=COLORS['muted'], bd=0)
        self.infoText.grid(row=0, column=0, sticky='nsew', padx=6, pady=6)

        # Log section
        logFrame = ttk.Frame(notebook, style='Dark.TFrame')
        self.logText = tk.Text(logFrame, height=8, bg=COLORS['bg'], fg=COLORS['muted'], bd=0)
        self.logText.pack(fill='both', expand=True, padx=6, pady=6)
        notebook.add(logFrame, text='Log')

        # Statusbar
        status = ttk.Frame(self, style='Dark.TFrame')
        status.pack(side='bottom', fill='x')
        self.statusLabel = ttk.Label(status, text='Ready', style='Dark.TLabel')
        self.statusLabel.pack(side='left', padx=8, pady=4)
        self.tree.bind('<<TreeviewSelect>>')
    
    def logMessage(self, msg: str):
        from datetime import datetime
        ts = datetime.now().strftime('%H:%M:%S')
        self.logText.insert('end', f'[{ts}] {msg}\n')
        self.logText.see('end')
        self.statusLabel.config(text=msg)

    def startGame(self):
        import subprocess
        try:
            subprocess.Popen([r"./game.exe"])
            self.logMessage('Ran start game')
        except Exception as e:
            self.logMessage(f'Error in starting: {e}')

    def resumeGame(self):
        import subprocess
        try:
            subprocess.Popen([r"./game.exe"])
            self.logMessage('Ran resume game')
        except Exception as e:
            self.logMessage(f'Error in resuming: {e}')

    def openFolder(self):
        import subprocess
        try:
            subprocess.check_call(["explorer", "additionalContent"])
            self.logMessage('Opened folder')
        except Exception as e:
            self.logMessage(f'Error in opening folder: {e}')

if __name__ == '__main__':
    app = mainApp()
    app.mainloop()

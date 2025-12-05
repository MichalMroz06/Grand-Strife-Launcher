import tkinter as tk
from tkinter import ttk
import platform
import json
from pathlib import Path

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
        
        # Dictionary for storing JSON data assigned to items
        self.itemsData = {}
        # Dictionary for storing JSON file paths
        self.itemsFilePath = {}

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
        
        # Text widget
        self.infoText = tk.Text(infoFrame, height=8, bg=COLORS['bg'], fg=COLORS['muted'], bd=0)
        self.infoText.grid(row=0, column=0, sticky='nsew', padx=6, pady=6)
        
        # Checkbox frame (hidden initially)
        self.checkboxFrame = ttk.Frame(infoFrame, style='Dark.TFrame')
        
        self.activeVar = tk.BooleanVar()
        self.activeCheckbox = ttk.Checkbutton(self.checkboxFrame, text='Active', variable=self.activeVar, 
                                              style='Dark.TButton', command=self.onActiveToggle)
        self.activeCheckbox.pack(side='left')
        
        # Store current selected item
        self.currentSelectedItem = None
        
        notebook.add(infoFrame, text='Info')

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

        self.tree.bind('<<TreeviewSelect>>', self.onTreeSelect)
        
        # Load items from folder (after creating all widgets)
        self.loadItemsFromFolder()


    def loadItemsFromFolder(self):
        """Loads config.json from each subfolder of 'additionalContent'"""
        folder_path = Path('additionalContent')
        
        if not folder_path.exists():
            self.logMessage('Folder "additionalContent" does not exist')
            return
        
        try:
            # Find config.json in every subfolder
            config_files = list(folder_path.glob('*/config.json'))
            
            if not config_files:
                self.logMessage('No config.json files found in subfolders')
                return
            
            for config_file in config_files:
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Add main item with JSON name and active indicator
                    item_name = data.get('name', config_file.parent.name)
                    active = data.get('active', False)
                    status_indicator = '✓' if active else '✗'
                    display_name = f"{status_indicator} {item_name}"
                    
                    parent = self.tree.insert('', 'end', text=display_name)
                    
                    # Store full JSON for this item
                    self.itemsData[parent] = data
                    # Store JSON file path
                    self.itemsFilePath[parent] = config_file
                    
                    self.logMessage(f'Loaded: {config_file.parent.name}/config.json')
                    
                except json.JSONDecodeError:
                    self.logMessage(f'Error: config.json in {config_file.parent.name} is not valid JSON')
                except Exception as e:
                    self.logMessage(f'Error reading {config_file.parent.name}/config.json: {e}')
        
        except Exception as e:
            self.logMessage(f'Error loading folder: {e}')

    def onTreeSelect(self, event=None):
        sel = self.tree.selection()
        if sel:
            item_id = sel[0]
            item = self.tree.item(item_id)
            
            # Remember currently selected item
            self.currentSelectedItem = item_id
            
            # Clear Info
            self.infoText.config(state='normal')
            self.infoText.delete('1.0', 'end')
            
            # Hide checkbox initially
            self.checkboxFrame.grid_forget()
            
            # If item has JSON data, display it
            if item_id in self.itemsData:
                data = self.itemsData[item_id]
                info_content = f"Name: {data.get('name', 'N/A')}\n"
                info_content += f"Version: {data.get('version', 'N/A')}\n"
                info_content += f"Info: {data.get('info', 'N/A')}\n"
                self.infoText.insert('end', info_content)
                
                # Set checkbox according to active attribute and show it
                active_value = data.get('active', False)
                self.activeVar.set(active_value)
                self.checkboxFrame.grid(row=1, column=0, sticky='ew', padx=6, pady=(0,6))
            
            self.infoText.config(state='disabled')

    def onActiveToggle(self):
        """Updates 'active' attribute in JSON file when checkbox is toggled"""
        if self.currentSelectedItem and self.currentSelectedItem in self.itemsData:
            data = self.itemsData[self.currentSelectedItem]
            data['active'] = self.activeVar.get()
            
            # Update Treeview text with new indicator
            item_name = data.get('name', 'Item')
            status_indicator = '✓' if data['active'] else '✗'
            display_name = f"{status_indicator} {item_name}"
            self.tree.item(self.currentSelectedItem, text=display_name)
            
            # Save changes to JSON
            self.saveItemToJSON(self.currentSelectedItem)
            self.logMessage(f"Active set to: {data['active']}")
    
    def saveItemToJSON(self, item_id):
        """Saves item JSON data to its file"""
        if item_id in self.itemsData and item_id in self.itemsFilePath:
            try:
                data = self.itemsData[item_id]
                file_path = self.itemsFilePath[item_id]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                self.logMessage(f'Saved: {file_path.name}')
            except Exception as e:
                self.logMessage(f'Error saving: {e}')
            
            self.logMessage(f"Active set to: {data['active']}")

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

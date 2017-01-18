'''
Created on Jan 18, 2017

@author: lubo
'''
import matplotlib as mpl
mpl.use('TkAgg')

from matplotlib.backends.backend_tkagg import *  # @UnusedWildImport @IgnorePep8
from matplotlib.figure import Figure  # @IgnorePep8 @Reimport

if sys.version_info[0] < 3:
    import Tkinter as tk  # @UnusedImport @UnresolvedImport
    import ttk  # @UnusedImport @UnresolvedImport
    from tkFileDialog import askopenfilename  # @UnusedImport @UnresolvedImport
    import tkMessageBox as messagebox  # @UnusedImport @UnresolvedImport
else:
    import tkinter as tk  # @Reimport @UnresolvedImport
    from tkinter import ttk  # @UnresolvedImport @UnusedImport @Reimport
    from tkinter.filedialog \
        import askopenfilename  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter.filedialog \
        import askdirectory  # @UnresolvedImport @Reimport@UnusedImport

    from tkinter import messagebox  # @UnresolvedImport @Reimport @UnusedImport


class CanvasWindow(object):

    def __init__(self, root):
        self.root = root

        self.fig = Figure(figsize=(12, 8))

        self.content = tk.Frame(self.root)
        self.content.pack(side="top", fill="both", expand=True)

        self.canvas = FigureCanvasTkAgg(self.fig, self.content)
        self.canvas.show()

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.content)
        self.toolbar.update()

        self.toolbar_ext = ttk.Frame(
            self.content,
            # relief='sunken',
            borderwidth=5,
            # width=150
        )
        self.button_ext = ttk.Frame(
            self.content, borderwidth=5,
            # width=150
        )

        self.toolbar.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvas.get_tk_widget().grid(
            column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.toolbar_ext.grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.button_ext.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.content.columnconfigure(0, weight=99)
        self.content.rowconfigure(0, weight=0)
        self.content.columnconfigure(1, weight=0)
        self.content.rowconfigure(1, weight=99)

        self._build_button_ext()

        self.on_controller_callbacks = []

    def register_on_controller_callback(self, cb):
        self.on_controller_callbacks.append(cb)

    def connect_controller(self, controller):
        for cb in self.on_controller_callbacks:
            cb(controller)
        self.canvas.draw()

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _build_button_ext(self):
        extframe = ttk.Frame(
            self.button_ext,
            # relief='sunken',
            borderwidth=5, width=150, height=100)
        extframe.grid(row=100, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.quit_button = ttk.Button(
            master=self.button_ext,
            text='Quit',
            command=self._quit)
        self.quit_button.grid(row=50, column=0)

        self.button_ext.rowconfigure(100, weight=100)

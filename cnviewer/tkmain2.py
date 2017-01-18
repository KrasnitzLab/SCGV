'''
Created on Jan 16, 2017

@author: lubo
'''
import sys  # @UnusedImport

import matplotlib
matplotlib.use('TkAgg')

from tkutils.profiles_ui import ProfilesUi
from tkutils.open_ui import OpenUi


from utils.model import DataModel  # @IgnorePep8
from views.controller import MainController  # @IgnorePep8


# @UnusedWildImport @IgnorePep8
from matplotlib.backends.backend_tkagg import *
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


class MainWindow(object):

    def __init__(self, root):
        self.model = None
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

    def connect_controller_callbacks(self, controller):
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


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("cnviewer")

    main = MainWindow(root)

    profiles = ProfilesUi(main.button_ext)
    profiles.build_ui()
    main.register_on_controller_callback(profiles.connect_controller)

    open_buttons = OpenUi(main, main.toolbar_ext, main.fig)
    open_buttons.build_ui()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()

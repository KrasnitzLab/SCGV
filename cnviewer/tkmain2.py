'''
Created on Jan 16, 2017

@author: lubo
'''

import matplotlib
matplotlib.use('TkAgg')


from utils.model import DataModel
from views.controller import MainController

import sys
import numpy as np


from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


# implement the default mpl key bindings


if sys.version_info[0] < 3:
    import Tkinter as tk  # @UnusedImport
    import ttk  # @UnusedImport
else:
    import tkinter as tk  # @Reimport @UnresolvedImport
    from tkinter import ttk  # @UnresolvedImport @UnusedImport @Reimport


class MainWindow(object):

    def __init__(self, root, fig):
        self.root = root

        self.fig = fig

        self.content = tk.Frame(self.root)
        self.content.pack(side="top", fill="both", expand=True)

        self.canvas = FigureCanvasTkAgg(self.fig, self.content)
        self.canvas.show()

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.content)
        self.toolbar.update()

        self.toolbar_ext = ttk.Frame(
            self.content, relief='sunken', borderwidth=5, width=150)
        self.button_ext = ttk.Frame(
            self.content, borderwidth=5, width=150)

        self.toolbar.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvas.get_tk_widget().grid(
            column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.toolbar_ext.grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.button_ext.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.content.columnconfigure(0, weight=99)
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(1, weight=1)
        self.content.rowconfigure(1, weight=99)

        self._build_quit_button()

        self._build_open_button()

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _build_quit_button(self):
        self.quit_button = ttk.Button(
            master=self.button_ext,
            text='Quit',
            command=self._quit)
        self.quit_button.pack()

    def _build_open_button(self):
        self.open_archive_button = ttk.Button(
            master=self.toolbar_ext,
            width=2,
            text="OA",
            command=self._open_archive)
        self.open_archive_button.grid(column=0, row=0)
        self.open_dir_button = ttk.Button(
            master=self.toolbar_ext,
            width=2,
            text="OD",
            command=self._open_archive)
        self.open_dir_button.grid(column=1, row=0)

    def _open_archive(self):
        print("opening archive...")

    def _open_dir(self):
        print("opening directory...")


def build_figure():
    f = Figure(figsize=(12, 8))
    a = f.add_subplot(111)
    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2 * np.pi * t)

    a.plot(t, s)
    a.set_title('Tk embedding')
    a.set_xlabel('X axis label')
    a.set_ylabel('Y label')
    return f


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("cnviewer")

    fig = build_figure()

    main = MainWindow(root, fig)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()

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
            self.content, borderwidth=5, relief="sunken", width=200)
        self.button_ext = ttk.Frame(
            self.content, borderwidth=5, relief="sunken", width=200)

        self.toolbar.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvas.get_tk_widget().grid(
            column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.toolbar_ext.grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.button_ext.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.content.columnconfigure(0, weight=99)
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(1, weight=1)
        self.content.rowconfigure(1, weight=99)


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

root = tk.Tk()
root.wm_title("cnviewer")

fig = build_figure()

main = MainWindow(root, fig)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()

# content = ttk.Frame(root, padding=(3, 3, 12, 12))
# frame = ttk.Frame(
#     content, borderwidth=5, relief="sunken", width=200, height=100)
# namelbl = ttk.Label(content, text="Name")
# name = ttk.Entry(content)
#
# onevar = tk.BooleanVar()
# twovar = tk.BooleanVar()
# threevar = tk.BooleanVar()
#
# onevar.set(True)
# twovar.set(False)
# threevar.set(True)
#
# one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
# two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
# three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
# ok = ttk.Button(content, text="Okay")
# cancel = ttk.Button(content, text="Cancel")
#
# content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
# frame.grid(column=0, row=0, columnspan=3, rowspan=2,
#            sticky=(tk.N, tk.S, tk.E, tk.W))
# namelbl.grid(column=3, row=0, columnspan=2, sticky=(tk.N, tk.W), padx=5)
# name.grid(column=3, row=1, columnspan=2,
#           sticky=(tk.N, tk.E, tk.W), pady=5, padx=5)
# one.grid(column=0, row=3)
# two.grid(column=1, row=3)
# three.grid(column=2, row=3)
# ok.grid(column=3, row=3)
# cancel.grid(column=4, row=3)
#
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
# content.columnconfigure(0, weight=3)
# content.columnconfigure(1, weight=3)
# content.columnconfigure(2, weight=3)
# content.columnconfigure(3, weight=1)
# content.columnconfigure(4, weight=1)
# content.rowconfigure(1, weight=1)

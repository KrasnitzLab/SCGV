'''
Created on Jan 11, 2017

@author: lubo
'''


import sys

import matplotlib
matplotlib.use('TkAgg')

from utils.model import DataModel
from views.controller import MainController


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

root = tk.Tk()
root.wm_title("cnviewer")


model = DataModel('tests/data/cnviewer_data_example_01.zip')
model.make()

mfig = plt.figure(0, figsize=(12, 8))
mfig.suptitle("cnviewer_data_example_01", fontsize=14)
main = MainController(model)
main.build_main(mfig)


main_frame = tk.Frame(root)
main_frame.pack()

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(mfig, main_frame)
canvas.show()

toolbar = NavigationToolbar2TkAgg(canvas, main_frame)
toolbar.update()
toolbar.pack(side=tk.TOP)

canvas._tkcanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = tk.Button(master=main_frame, text='Quit', command=_quit)
button.pack(side=tk.RIGHT)

tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.

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
    import Tkinter as Tk  # @UnusedImport
else:
    import tkinter as Tk  # @Reimport @UnresolvedImport

root = Tk.Tk()
root.wm_title("cnviewer")


model = DataModel('tests/data/cnviewer_data_example_01.zip')
model.make()

mfig = plt.figure(0, figsize=(12, 8))
mfig.suptitle("cnviewer_data_example_01", fontsize=14)
main = MainController(model)
main.build_main(mfig)


mainFrame = Tk.Frame(root)
mainFrame.pack()

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(mfig, mainFrame)
canvas.show()

toolbar = NavigationToolbar2TkAgg(canvas, mainFrame)
toolbar.update()
toolbar.pack(side=Tk.TOP)

canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
canvas.get_tk_widget().pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = Tk.Button(master=mainFrame, text='Quit', command=_quit)
button.pack(side=Tk.RIGHT)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.

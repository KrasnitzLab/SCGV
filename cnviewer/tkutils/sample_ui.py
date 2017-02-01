'''
Created on Jan 18, 2017

@author: lubo
'''

import sys  # @UnusedImport
from tkutils.canvas_ui import CanvasWindow
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


class SampleUi(object):

    def __init__(self, sample_list):
        self.root = tk.Toplevel()
        self.sample_list = sample_list[:]

    def build_ui(self):
        self.main = CanvasWindow(self.root, legend=False)
        return self.main.fig

    def mainloop(self):
        self.root.mainloop()

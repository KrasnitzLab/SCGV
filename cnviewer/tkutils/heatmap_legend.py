'''
Created on Feb 8, 2017

@author: lubo
'''
import sys  # @UnusedImport

if sys.version_info[0] < 3:
    import Tkinter as tk  # @UnusedImport @UnresolvedImport
    import ttk  # @UnusedImport @UnresolvedImport
    from tkFileDialog import askopenfilename  # @UnusedImport @UnresolvedImport
    import tkMessageBox as messagebox  # @UnusedImport @UnresolvedImport
else:
    import tkinter as tk  # @Reimport @UnresolvedImport @UnusedImport
    from tkinter import ttk  # @UnresolvedImport @UnusedImport @Reimport
    from tkinter.filedialog \
        import askopenfilename  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter.filedialog \
        import askdirectory  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter import messagebox  # @UnresolvedImport @Reimport @UnusedImport


class HeatmapLegend(object):

    def __init__(self, master):
        self.master = master

    def build_ui(self):

        frame = ttk.Frame(
            self.master,
            borderwidth=5,
            relief='sunken',
        )
        frame.grid(row=20, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        label = ttk.Label(frame, text="Heatmap Legend")
        label.grid(column=0, row=0, columnspan=2)

        scrollbar = ttk.Scrollbar(
            frame, orient=tk.VERTICAL)
        scrollbar.grid(column=1, row=1, sticky=(tk.N, tk.S))

        self.canvas = tk.Canvas(
            frame,
            yscrollcommand=scrollbar.set,
            height=80, width=50)
        self.canvas.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.config(command=self.canvas.yview)

        def configure_update(event):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.canvas.bind(
            '<Configure>',
            configure_update)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(20, weight=1)

        self.container = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.container, anchor='nw')

        l = tk.Label(
            self.container,
            bitmap='',
            text="Hello")
        l.pack()

        l = tk.Label(self.container, text="World", font="-size 50")
        l.pack()

        l = tk.Label(
            self.container, text="Test text 1\nTest text 2\nTest text 3\nTest text 4\nTest text 5\nTest text 6\nTest text 7\nTest text 8\nTest text 9", font="-size 20")
        l.pack()

        configure_update(None)

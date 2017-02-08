'''
Created on Feb 8, 2017

@author: lubo
'''
import sys  # @UnusedImport
from PIL import Image, ImageTk

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
            height=100, width=100,
            background='white')
        self.canvas.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.config(command=self.canvas.yview)

        def configure_update(event):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.canvas.bind(
            '<Configure>',
            configure_update)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(20, weight=1)

        self.container = tk.Frame(self.canvas, background='white')
        self.canvas.create_window((0, 0), window=self.container, anchor='nw')

        image = Image.new('RGB', size=(20, 20), color=(255, 0, 0))
        self.bitmap = ImageTk.PhotoImage(image=image)

        def click_callback(val):
            return lambda event: print("click_callback({}) called".format(val))

        l = ttk.Label(
            self.container,
            text='text1',
            image=self.bitmap,
            compound=tk.LEFT)
        l.pack()
        l.bind('<Double-Button-1>', click_callback(1))

        image = Image.new('RGB', size=(20, 20), color=(0, 255, 0))
        self.bitmap2 = ImageTk.PhotoImage(image=image)

        l = ttk.Label(
            self.container,
            text='text1',
            image=self.bitmap2,
            compound=tk.LEFT)
        l.pack()
        l.bind('<Double-Button-1>', click_callback(2))

        configure_update(None)

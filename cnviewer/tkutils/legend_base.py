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


class LegendEntry(object):
    IMAGE_SIZE = 15

    def __init__(self, index, text, color):
        self.index = index
        self.text = text
        self.color = color
        self.image = None
        if color:
            tkcolor = self.tkcolor(color)
            image = Image.new(
                'RGB',
                size=(self.IMAGE_SIZE, self.IMAGE_SIZE),
                color=tkcolor)
            self.image = ImageTk.PhotoImage(image=image)

    @staticmethod
    def tkcolor(color):
        if len(color) == 3:
            r, g, b = color
            a = 1
        elif len(color) == 4:
            r, g, b, a = color
        else:
            raise ValueError("strange color: {}".format(str(color)))
        return (int(255 * r), int(255 * g), int(255 * b), int(255 * a))

    def build_label(self, master):
        self.label = ttk.Label(
            master,
            text=self.text,
            image=self.image,
            compound=tk.LEFT,
            background='white',
        )
        self.label.pack(anchor=tk.W)

    def bind_dbl_click(self, callback):
        def click_callback(index):
            return lambda event: callback(index)

        self.label.bind('<Double-Button-1>', click_callback(self.index))


class LegendBase(object):

    def __init__(self, master, title):
        self.master = master
        self.title = title

    def build_ui(self, row=20):
        frame = ttk.Frame(
            self.master,
            borderwidth=5,
            relief='sunken',
        )
        frame.grid(row=row, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        label = ttk.Label(frame, text=self.title)
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

        self.entries = []
        configure_update(None)

    def append_entry(self, text, color=None):
        index = len(self.entries)
        entry = LegendEntry(index, text, color)
        entry.build_label(self.container)
        self.entries.append(entry)

    def bind_dbl_click(self, callback):
        for entry in self.entries:
            entry.bind_dbl_click(callback)

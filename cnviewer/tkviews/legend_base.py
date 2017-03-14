'''
Created on Feb 8, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport

import matplotlib.colors as col

from PIL import Image, ImageTk
from tkviews.base_ui import BaseUi


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
                'RGBA',
                size=(self.IMAGE_SIZE, self.IMAGE_SIZE),
                color=tkcolor)
            self.image = ImageTk.PhotoImage(image=image)

    @staticmethod
    def tkcolor(color):
        c = col.to_rgba(color)
        if len(c) == 3:
            r, g, b = color
            a = 1
        elif len(c) == 4:
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

    def bind_dbl_left_click(self, callback):
        def click_callback(index):
            return lambda event: callback(index)
        self.label.bind('<Double-Button-1>', click_callback(self.index))

    def bind_dbl_right_click(self, callback):
        def click_callback(index):
            return lambda event: callback(index)
        self.label.bind('<Double-Button-3>', click_callback(self.index))

    def bind_right_click(self, callback):
        def click_callback(index):
            return lambda event: callback(index)
        self.label.bind('<Button-3>', click_callback(self.index))


class LegendBase(BaseUi):

    def __init__(self, master, title, controller, subject):
        super(LegendBase, self).__init__(master, controller, subject)
        self.title = title

    def enable_ui(self):
        pass

    def build_ui(self, row=20):
        self.entries = []
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

        # self.connect_controller()
        configure_update(None)

    def append_entry(self, text, color=None):
        index = len(self.entries)
        entry = LegendEntry(index, text, color)
        entry.build_label(self.container)
        self.entries.append(entry)

    def configure_update(self, *args, **kwargs):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def bind_dbl_left_click(self, callback):
        for entry in self.entries:
            entry.bind_dbl_left_click(callback)

    def bind_dbl_right_click(self, callback):
        for entry in self.entries:
            entry.bind_dbl_right_click(callback)

    def bind_right_click(self, callback):
        for entry in self.entries:
            entry.bind_right_click(callback)

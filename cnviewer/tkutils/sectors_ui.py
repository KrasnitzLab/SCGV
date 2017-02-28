'''
Created on Jan 18, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport

from tkutils.base_ui import BaseUi


class SectorsUi(BaseUi):

    def __init__(self, master, controller):
        super(SectorsUi, self).__init__(master, controller)
        self.sectors_reorder_callbacks = []

    def build_ui(self):
        frame = ttk.Frame(
            self.master,
            borderwidth=5)
        frame.grid(
            row=40, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.show_sectors = ttk.Button(
            master=frame, text="Sectors Reorder", command=self._show_sectors)
        self.show_sectors.config(state=tk.DISABLED)

        self.show_sectors.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        super(SectorsUi, self).build_ui()

    def enable_ui(self):
        if self.model.sector is None:
            return
        self.show_sectors.config(state=tk.ACTIVE)

    def disable_ui(self):
        self.show_sectors.config(state=tk.DISABLED)

    def register_on_sectors_reorder(self, cb):
        self.sectors_reorder_callbacks.append(cb)

    def _show_sectors(self):
        for cb in self.sectors_reorder_callbacks:
            cb(self)

'''
Created on Jan 18, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport
from tkutils.base_ui import BaseUi


class PinmatUi(BaseUi):

    def __init__(self, master, controller):
        super(PinmatUi, self).__init__(master, controller)
        self.pinmat_callbacks = []

    def build_ui(self):
        frame = ttk.Frame(
            self.master,
            borderwidth=5)
        frame.grid(
            row=30, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.show_pinmat = ttk.Button(
            master=frame, text="Show Pins", command=self._show_pinmat)
        self.show_pinmat.config(state=tk.DISABLED)

        self.show_pinmat.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        super(PinmatUi, self).build_ui()

    def register_on_pinmat(self, callback):
        self.pinmat_callbacks.append(callback)

    def _show_pinmat(self):
        print("show pins called...")
        assert self.controller is not None

        for cb in self.pinmat_callbacks:
            cb(self)

    def enable_ui(self):
        self.show_pinmat.config(state=tk.ACTIVE)

    def disable_ui(self):
        self.show_pinmat.config(state=tk.DISABLED)

'''
Created on Feb 1, 2017

@author: lubo
'''
import sys  # @UnusedImport
import os

from PIL import ImageTk, Image

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


class SectorsLegend(object):

    def __init__(self, master):
        self.master = master

    def build_ui(self):

        self.sectors_ui = tk.Listbox(
            self.master, height=5)
        self.sectors_ui.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        s = ttk.Scrollbar(

            self.master, orient=tk.VERTICAL, command=self.sectors_ui.yview)
        s.grid(column=1, row=0, sticky=(tk.N, tk.S))
        self.sectors_ui['yscrollcommand'] = s.set

    def register_controller(self, controller):
        self.controller = controller
        self.sectors = self.controller.model.make_sectors_legend()

        for (sector, pathology) in self.sectors:
            self.sectors_ui.insert(tk.END, '{}: {}'.format(sector, pathology))

        self.sectors_ui.bind('<Double-Button-1>', self.show_sector)

    def show_sector(self, event):
        (index,) = self.sectors_ui.curselection()
        (sector, pathology) = self.sectors[index]
        print(self.sectors)
        print(sector, pathology)
        if self.controller.model.pathology is None:
            return
        filename = self.controller.model.pathology.get(pathology, None)
        if filename is None or not os.path.exists(filename):
            return
        print("loading: ", filename)

        self.window = tk.Toplevel(self.master)
        self.window.title(pathology)
        self.window.geometry("500x500")
        self.window.configure(background='grey')
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        image = ImageTk.PhotoImage(Image.open(filename))
        panel = tk.Label(self.window, image=image)
        panel.pack(side="bottom", fill="both", expand="yes")

        self.window.mainloop()

    def on_closing(self):
        self.window.quit()     # stops mainloop
        self.window.destroy()  # this is necessary on Windows to prevent

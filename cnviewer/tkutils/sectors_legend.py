'''
Created on Feb 1, 2017

@author: lubo
'''
import sys  # @UnusedImport

from PIL import ImageTk

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

        frame = ttk.Frame(
            self.master,
            borderwidth=5,
            relief='sunken',
        )
        frame.grid(row=10, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        label = ttk.Label(frame, text="Sectors Legend")
        label.grid(column=0, row=0, columnspan=2)

        self.sectors_ui = tk.Listbox(
            frame, height=5)
        self.sectors_ui.grid(
            column=0, row=10, sticky=(tk.N, tk.S, tk.E, tk.W))
        s = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=self.sectors_ui.yview)
        s.grid(column=1, row=10, sticky=(tk.N, tk.S))
        self.sectors_ui['yscrollcommand'] = s.set

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(10, weight=1)

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
        image = self.controller.model.pathology.get(pathology, None)
        if image is None:
            return

        window = tk.Toplevel()
        window.title(pathology)
        window.configure(background='grey')

        def on_close():
            window.quit()     # stops mainloop
            window.destroy()  # this is necessary on Windows to prevent

        window.protocol("WM_DELETE_WINDOW", on_close)

        image = ImageTk.PhotoImage(image)
        panel = tk.Label(window, image=image)
        panel.pack(side="bottom", fill="both", expand="yes")
        window.mainloop()

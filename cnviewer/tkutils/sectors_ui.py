'''
Created on Jan 18, 2017

@author: lubo
'''
import sys  # @UnusedImport
from tkutils.canvas_ui import CanvasWindow
from controllers.controller import MainController
from tkutils.profiles_ui import ProfilesUi
from models.sector_model import SectorDataModel
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


class SectorsWindow(CanvasWindow):

    def __init__(self, root):
        super(SectorsWindow, self).__init__(root)
        profiles = ProfilesUi(self.button_ext, self)
        profiles.build_ui()
        self.register_on_controller_callback(profiles.connect_controller)


class SectorsUi(object):

    def __init__(self, master):
        self.master = master
        self.controller = None
        self.root = None

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

    def _show_sectors(self):
        self.show_sectors.config(state=tk.DISABLED)

        print("_show_sectors called...")
        if self.controller is None:
            return
        assert self.controller is not None

        sector_model = SectorDataModel(self.controller.model)
        sector_model.make()
        controller = MainController(sector_model)

        self.root = tk.Toplevel()
        main = SectorsWindow(self.root)

        controller.build_sector(main.fig)
        main.connect_controller(controller)
        main.register_on_closing_callback(self.on_closing)

        self.root.mainloop()

    def on_closing(self):
        print("SectorsUi::on_closing called...")
        self.show_sectors.config(state=tk.ACTIVE)

    def connect_controller(self, controller):
        assert controller is not None
        self.controller = controller

        self.show_sectors.config(state=tk.ACTIVE)

'''
Created on Feb 1, 2017

@author: lubo
'''
import sys  # @UnusedImport

from PIL import ImageTk
from tkutils.legend_base import LegendBase
from utils.color_map import ColorMap
# from utils.sector_model import SingleSectorDataModel
# from views.controller import MainController
# from tkutils.sectors_ui import SectorsWindow

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


# from utils.sector_model import SingleSectorDataModel
# from views.controller import MainController
# from tkutils.sectors_ui import SectorsWindow


class SectorsLegend2(LegendBase):

    def __init__(self, master):
        super(SectorsLegend2, self).__init__(
            master, title="Sectors Legend")
        self.controller = None

    def register_controller(self, controller):
        self.controller = controller
        self.sectors = self.controller.model.make_sectors_legend()
        self.cmap = ColorMap.make_qualitative12()

        for (index, (sector, pathology)) in enumerate(self.sectors):
            color = self.cmap.colors(index)
            print(color)
            self.append_entry(
                text='{}: {}'.format(sector, pathology),
                color=color)

        self.bind_dbl_right_click(self.show_sector_pathology)
        self.bind_dbl_left_click(self.show_single_sector)

    def register_show_single_sector_callback(self, callback):
        self.show_single_sector_callback = callback

    def show_sector_pathology(self, index):
        print("show sector pathology with index: ", index)
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

    def connect_controller(self, controller):
        assert controller is not None
        self.controller = controller

    def show_single_sector(self, index):
        print("show single sector viewer with index: ", index)
        (sector, _) = self.sectors[index]
        print("working with sector: ", sector)

        self.show_single_sector_callback(self.controller.model, sector)

#
#         root = tk.Toplevel()
#         main = SectorsWindow(root)
#         controller.build_sector(main.fig)
#
#         main.connect_controller(controller)
#
#         def on_closing():
#             pass
#         main.register_on_closing_callback(on_closing)
#         root.mainloop()

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
    import tkSimpleDialog as simpledialog  # @UnusedImport @UnresolvedImport
else:
    import tkinter as tk  # @Reimport @UnresolvedImport @UnusedImport
    from tkinter import ttk  # @UnresolvedImport @UnusedImport @Reimport
    from tkinter.filedialog \
        import askopenfilename  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter.filedialog \
        import askdirectory  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter import messagebox  # @UnresolvedImport @Reimport @UnusedImport
    # @UnresolvedImport @Reimport @UnusedImport @IgnorePep8
    from tkinter import simpledialog


# from utils.sector_model import SingleSectorDataModel
# from views.controller import MainController
# from tkutils.sectors_ui import SectorsWindow


class PathologyDialog(simpledialog.Dialog):

    def __init__(self, image, notes, master, **kwargs):
        self.image = image
        self.notes = notes
        super(PathologyDialog, self).__init__(master, **kwargs)

    def body(self, master):
        self.image = ImageTk.PhotoImage(self.image)
        panel = tk.Label(master, image=self.image)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        text = tk.Text(master, width=80, height=20)
        scrollbar = tk.Scrollbar(master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        scrollbar.config(command=text.yview)
        text.config(yscrollcommand=scrollbar.set)

        text.tag_configure('big', font=('Verdana', 15, 'bold'))
        text.insert(tk.END, self.notes[0], 'big')
        for line in self.notes[1:]:
            text.insert(tk.END, line)

        return panel

    def apply(self):
        return None


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

        self.bind_right_click(self.show_sector_pathology)
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
        image, notes = self.controller.model.pathology.get(pathology, None)
        if image is None and notes is None:
            return

        PathologyDialog(image, notes, self.master)
        print("pathology dialog done...")

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

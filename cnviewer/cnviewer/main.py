'''
Created on Feb 8, 2017

@author: lubo
'''
import sys  # @UnusedImport
from tkutils.canvas_ui import CanvasWindow


from tkutils.profiles_ui import ProfilesUi
from tkutils.open_ui import OpenUi
from tkutils.pinmat_ui import PinmatUi
from tkutils.sectors_ui import SectorsUi, SectorsWindow
from tkutils.sectors_legend2 import SectorsLegend2
from tkutils.heatmap_legend import HeatmapLegend
from utils.sector_model import SingleSectorDataModel
from views.controller import MainController


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


def show_single_sector(model, sector_id):
    sector_model = SingleSectorDataModel(model, sector_id)
    sector_model.make()

    controller = MainController(sector_model)

    root = tk.Toplevel()
    main = SectorsWindow(root)
    controller.build_sector(main.fig)

    main.connect_controller(controller)

    root.mainloop()


def main():
    root = tk.Tk()
    root.wm_title("cnviewer")

    main = CanvasWindow(root)

    profiles = ProfilesUi(main.button_ext)
    profiles.build_ui()
    main.register_on_controller_callback(profiles.connect_controller)

    pinmat = PinmatUi(main.button_ext)
    pinmat.build_ui()
    main.register_on_controller_callback(pinmat.connect_controller)

    sectors = SectorsUi(main.button_ext)
    sectors.build_ui()
    main.register_on_controller_callback(sectors.connect_controller)

    sectors_legend = SectorsLegend2(main.legend_ext)
    sectors_legend.build_ui(row=10)
    sectors_legend.register_show_single_sector_callback(show_single_sector)
    main.register_on_controller_callback(sectors_legend.register_controller)

    heatmap_legend = HeatmapLegend(main.legend_ext)
    heatmap_legend.build_ui()
    heatmap_legend.show_legend()

    open_buttons = OpenUi(main, main.button_ext, main.fig)
    open_buttons.build_ui()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()

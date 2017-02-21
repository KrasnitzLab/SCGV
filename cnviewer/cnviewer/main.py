'''
Created on Feb 8, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport

from tkutils.sectors_ui import SectorsWindow
from models.sector_model import SingleSectorDataModel
from controllers.controller import MainController
from cnviewer.main_window import MainWindow


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

    controller = MainController()
    main = MainWindow(root, controller)
    main.build_ui()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()

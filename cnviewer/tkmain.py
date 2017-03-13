'''
Created on Jan 16, 2017

@author: lubo
'''
import matplotlib as mpl
mpl.use('TkAgg')

from tkviews.tkimport import *  # @UnusedWildImport @NoMove @IgnorePep8

# from models.sector_model import SingleSectorDataModel
from controllers.controller import MainController  # @IgnorePep8
from tkviews.main_window import MainWindow  # @IgnorePep8


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

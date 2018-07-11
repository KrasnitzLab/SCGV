'''
Created on Jan 16, 2017

@author: lubo
'''
import matplotlib as mpl
from scgv.models.subject import DataSubject, ProfilesSubject
from scgv.commands.executor import CommandExecutor
mpl.use('TkAgg')

from scgv.tkviews.tkimport import *  # @UnusedWildImport @NoMove @IgnorePep8

# from models.sector_model import SingleSectorDataModel
from scgv.controllers.controller import MainController  # @IgnorePep8
from scgv.tkviews.main_window import MainWindow  # @IgnorePep8


def main():
    root = tk.Tk()
    root.wm_title("SCGV")

    CommandExecutor.start(root)

    data_subject = DataSubject()
    profiles_subject = ProfilesSubject()

    controller = MainController()
    main = MainWindow(
        root, controller, data_subject, profiles_subject)
    main.build_ui()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()

'''
Created on Mar 14, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport
from models.pinmat_model import PinmatModel
from controllers.controller import PinmatController, SectorsController
from models.subject import DataSubject, ProfilesSubject
from tkviews.base_window import BaseHeatmapWindow
from commands.executor import CommandExecutor
from commands.command import Command
from models.sector_model import SectorsDataModel
from tkviews.sectors_window import SectorsWindow


class ShowPinsCommand(Command):

    def __init__(self, model, on_close):
        assert isinstance(on_close, Command)

        self.model = model
        self.on_close = on_close

    def execute(self):
        root = tk.Toplevel()
        model = PinmatModel(self.model)
        # model.make()

        controller = PinmatController(model)
        data_subject = DataSubject()
        profiles_subject = ProfilesSubject()

        pinmat_window = BaseHeatmapWindow(
            root, controller, data_subject, profiles_subject)
        pinmat_window.build_ui()

        def on_close():
            CommandExecutor.execute(self.on_close)
        pinmat_window.register_on_closing_callback(on_close)

        data_subject.set_model(model)

        root.mainloop()


class ShowSectorsReorderCommand(Command):

    def __init__(self, model, on_close):
        assert isinstance(on_close, Command)

        self.model = model
        self.on_close = on_close

    def execute(self):
        root = tk.Toplevel()
        sectors_model = SectorsDataModel(self.model)
        sectors_model.make()

        controller = SectorsController(sectors_model)
        data_subject = DataSubject()
        profiles_subject = ProfilesSubject()

        sectors_window = SectorsWindow(
            root, controller, data_subject, profiles_subject)
        sectors_window.build_ui()

        def on_close():
            CommandExecutor.execute(self.on_close)
        sectors_window.register_on_closing_callback(on_close)

        data_subject.set_model(sectors_model)
        root.mainloop()

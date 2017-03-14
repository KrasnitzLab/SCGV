'''
Created on Mar 14, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport
from models.pinmat_model import PinmatModel
from controllers.controller import PinmatController, SectorsController
from models.subject import DataSubject
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
        subject = DataSubject()
        pinmat_window = BaseHeatmapWindow(root, controller, subject)
        pinmat_window.build_ui()

        subject.set_model(model)

        def on_close():
            CommandExecutor.execute(self.on_close)
        pinmat_window.register_on_closing_callback(on_close)

        pinmat_window.draw_canvas()
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
        subject = DataSubject()
        sectors_window = SectorsWindow(root, controller, subject)
        sectors_window.build_ui()

        subject.set_model(sectors_model)

        def on_close():
            CommandExecutor.execute(self.on_close)
        sectors_window.register_on_closing_callback(on_close)

        sectors_window.draw_canvas()
        root.mainloop()

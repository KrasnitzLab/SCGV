'''
Created on Feb 21, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport


from tkviews.open_ui import OpenUi
from tkviews.pinmat_ui import PinmatUi
from tkviews.sectors_ui import SectorsUi

from tkviews.base_window import BaseHeatmapWindow

from models.sector_model import SectorsDataModel
from tkviews.sectors_window import SectorsWindow
from models.pinmat_model import PinmatModel
from controllers.controller import PinmatController, SectorsController
from models.subject import DataSubject


class MainWindow(BaseHeatmapWindow):

    def __init__(self, master, controller, subject):
        super(MainWindow, self).__init__(master, controller, subject)
        self.controller.register_on_model_callback(self.on_model_callback)

    def build_ui(self):
        self.build_base_ui()

        pinmat = PinmatUi(
            self.main.button_ext, self.controller, self.subject)
        pinmat.build_ui()
        pinmat.register_on_pinmat(self.build_pinmat)

        sectors = SectorsUi(
            self.main.button_ext, self.controller, self.subject)
        sectors.build_ui()
        sectors.register_on_sectors_reorder(self.build_sectors_reorder)

        open_buttons = OpenUi(self.main.button_ext, self.subject)
        open_buttons.build_ui()

    def on_model_callback(self, model):
        self.model = model
        self.draw_canvas()

    def build_pinmat(self, pinmat_button):
        pinmat_button.disable_ui()

        root = tk.Toplevel()
        model = PinmatModel(self.model)
        # model.make()

        controller = PinmatController(model)
        pinmat_window = BaseHeatmapWindow(root, controller)
        pinmat_window.build_ui()

        def on_close():
            pinmat_button.enable_ui()
        pinmat_window.register_on_closing_callback(on_close)

        pinmat_window.draw_canvas()
        root.mainloop()

    def build_sectors_reorder(self, sectors_button):
        sectors_button.disable_ui()

        root = tk.Toplevel()
        sectors_model = SectorsDataModel(self.model)
        sectors_model.make()

        controller = SectorsController(sectors_model)
        subject = DataSubject()
        sectors_window = SectorsWindow(root, controller, subject)
        sectors_window.build_ui()

        subject.set_model(sectors_model)

        def on_close():
            sectors_button.enable_ui()
        sectors_window.register_on_closing_callback(on_close)

        sectors_window.draw_canvas()
        root.mainloop()

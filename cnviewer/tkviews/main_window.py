'''
Created on Feb 21, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport

from commands.command import MacroCommand
from commands.executor import CommandExecutor
from commands.show import ShowPinsCommand
from commands.show import ShowSectorsReorderCommand
from commands.widget import EnableCommand, DisableCommand
from tkviews.base_window import BaseHeatmapWindow
from tkviews.open_ui import OpenUi
from tkviews.pinmat_ui import PinmatUi
from tkviews.sectors_ui import SectorsUi


class MainWindow(BaseHeatmapWindow):

    def __init__(self, master, controller, subject):
        super(MainWindow, self).__init__(master, controller, subject)
        self.controller.register_on_model_callback(self.on_model_callback)

    def build_ui(self):
        self.build_base_ui()

        pinmat = PinmatUi(
            self.main.button_ext, self.controller, self.subject)
        pinmat.build_ui()
        pinmat.register_on_pinmat(self.show_pins)

        sectors = SectorsUi(
            self.main.button_ext, self.controller, self.subject)
        sectors.build_ui()
        sectors.register_on_sectors_reorder(self.build_sectors_reorder)

        open_buttons = OpenUi(self.main.button_ext, self.subject)
        open_buttons.build_ui()

    def on_model_callback(self, model):
        self.model = model
        self.draw_canvas()

    def show_pins(self, pinmat_button):
        disable_command = DisableCommand(pinmat_button.show_pinmat)
        show_pins = ShowPinsCommand(
            self.model, EnableCommand(pinmat_button.show_pinmat))
        macro = MacroCommand(disable_command, show_pins)
        CommandExecutor.execute(macro)

    def build_sectors_reorder(self, sectors_button):
        disable_command = DisableCommand(sectors_button.show_sectors)
        show_sectors = ShowSectorsReorderCommand(
            self.model, EnableCommand(sectors_button.show_sectors))
        macro = MacroCommand(disable_command, show_sectors)
        CommandExecutor.execute(macro)

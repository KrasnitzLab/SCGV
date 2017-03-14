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
from utils.observer import Observer


class PinsButton(Observer):

    def __init__(self, master, subject):
        super(PinsButton, self).__init__(subject)
        self.master = master

    def build_ui(self):
        frame = ttk.Frame(
            self.master,
            borderwidth=5)
        frame.grid(
            row=30, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.button = ttk.Button(
            master=frame, text="Show Pins", command=self._show_pinmat)
        self.button.config(state=tk.DISABLED)

        self.button.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def _show_pinmat(self):
        print("show pins called...")
        assert self.model is not None

        disable_command = DisableCommand(self.button)
        show_pins = ShowPinsCommand(
            self.model, EnableCommand(self.button))
        macro = MacroCommand(disable_command, show_pins)
        CommandExecutor.execute(macro)

    def update(self):
        self.model = self.get_model()
        if self.model is None or self.model.data.pins_df is None:
            return
        enable_command = EnableCommand(self.button)
        CommandExecutor.execute(enable_command)


class SectorsButton(Observer):

    def __init__(self, master, subject):
        super(SectorsButton, self).__init__(subject)
        self.master = master

    def build_ui(self):
        frame = ttk.Frame(
            self.master,
            borderwidth=5)
        frame.grid(
            row=40, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.button = ttk.Button(
            master=frame, text="Sectors Reorder", command=self._show_sectors)
        self.button.config(state=tk.DISABLED)

        self.button.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        # super(SectorsUi, self).build_ui()

    def update(self):
        self.model = self.get_model()

        if self.model is None or self.model.sector is None:
            return
        enable_command = EnableCommand(self.button)
        CommandExecutor.execute(enable_command)

    def _show_sectors(self):
        print("show sectors called...")
        assert self.model is not None

        disable_command = DisableCommand(self.button)
        show_sectors = ShowSectorsReorderCommand(
            self.model, EnableCommand(self.button))
        macro = MacroCommand(disable_command, show_sectors)
        CommandExecutor.execute(macro)


class MainWindow(BaseHeatmapWindow):

    def __init__(self, master, controller, subject):
        super(MainWindow, self).__init__(master, controller, subject)
        self.controller.register_on_model_callback(self.on_model_callback)

    def build_ui(self):
        self.build_base_ui()

        pinmat = PinsButton(
            self.main.button_ext, self.subject)
        pinmat.build_ui()

        sectors = SectorsButton(
            self.main.button_ext, self.subject)
        sectors.build_ui()

        open_buttons = OpenUi(self.main.button_ext, self.subject)
        open_buttons.build_ui()

    def on_model_callback(self, model):
        self.model = model
        self.draw_canvas()

'''
Created on Feb 21, 2017

@author: lubo
'''
from scgv.tkviews.tkimport import *  # @UnusedWildImport

from scgv.commands.command import MacroCommand, Command
from scgv.commands.executor import CommandExecutor
from scgv.commands.show import ShowFeaturesCommand
from scgv.commands.show import ShowSectorsReorderCommand
from scgv.commands.widget import EnableCommand, DisableCommand
from scgv.tkviews.base_window import BaseHeatmapWindow
from scgv.utils.observer import DataObserver
from scgv.commands.open import OpenCommand
from scgv.models.subject import DataSubject


class FeaturesButton(DataObserver):

    def __init__(self, master, subject):
        super(FeaturesButton, self).__init__(subject)
        self.master = master

    def build_ui(self):
        frame = ttk.Frame(
            self.master,
            borderwidth=5)
        frame.grid(
            row=30, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.button = ttk.Button(
            master=frame, text="Feature View", command=self._show_featuremat)
        self.button.config(state=tk.DISABLED)

        self.button.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def _show_featuremat(self):
        print("show features called...")
        assert self.model is not None

        disable_command = DisableCommand(self.button)
        show_features = ShowFeaturesCommand(
            self.model, EnableCommand(self.button))
        macro = MacroCommand(disable_command, show_features)
        CommandExecutor.execute_after(macro)

    def update(self, subject):
        assert isinstance(subject, DataSubject)

        self.model = self.get_model()
        if self.model is None or self.model.data.features_df is None:
            return
        enable_command = EnableCommand(self.button)
        CommandExecutor.execute_after(enable_command)


class SectorsButton(DataObserver):

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
            master=frame, text="Order by Sector", command=self._show_sectors)
        self.button.config(state=tk.DISABLED)

        self.button.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        # super(SectorsUi, self).build_ui()

    def update(self, subject):
        assert isinstance(subject, DataSubject)

        self.model = self.get_model()

        if self.model is None or self.model.sector is None:
            return
        enable_command = EnableCommand(self.button)
        CommandExecutor.execute_after(enable_command)

    def _show_sectors(self):
        print("show sectors called...")
        assert self.model is not None

        disable_command = DisableCommand(self.button)
        show_sectors = ShowSectorsReorderCommand(
            self.model, EnableCommand(self.button))
        macro = MacroCommand(disable_command, show_sectors)
        CommandExecutor.execute_after(macro)


class StartProgress(Command):

    def __init__(self, progress):
        self.progress = progress

    def execute(self):
        self.progress.grid(
            row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.progress.start()


class StopProgress(Command):

    def __init__(self, progress):
        self.progress = progress

    def execute(self):
        self.progress.stop()
        self.progress.grid_remove()


class OpenButtons(DataObserver):

    def __init__(self, master, subject):
        super(OpenButtons, self).__init__(subject)
        self.master = master

    def build_ui(self):
        frame = ttk.Frame(
            self.master,
            relief='flat',
            borderwidth=5
        )
        frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.open_archive_button = ttk.Button(
            master=frame,
            text="Open Archive",
            command=self._open_archive)
        self.open_archive_button.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.open_dir_button = ttk.Button(
            master=frame,
            text="Open Directory",
            command=self._open_dir)
        self.open_dir_button.grid(
            column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        progress_frame = ttk.Frame(
            master=frame,
            relief='flat',
            borderwidth=5,
            height=20,
        )
        progress_frame.grid(
            row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        progress_frame.columnconfigure(0, weight=99)

        self.progress = ttk.Progressbar(
            progress_frame, mode='indeterminate')
        # self.progress.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def _open_dir(self):
        filename = askdirectory()
        if not filename:
            print("open directory canceled...")
            return
        self._start_loading(filename)

    def _start_loading(self, filename):
        macro = MacroCommand(
            DisableCommand(self.open_archive_button),
            DisableCommand(self.open_dir_button),
            StartProgress(self.progress),
            OpenCommand(self.master, self.subject, filename)
        )
        CommandExecutor.execute_after(macro)

    def update(self, subject):
        assert isinstance(subject, DataSubject)

        macro = MacroCommand(StopProgress(self.progress))
        if self.get_model() is None:
            macro.add_command(EnableCommand(self.open_archive_button))
            macro.add_command(EnableCommand(self.open_dir_button))
        CommandExecutor.execute_after(macro)

    def _open_archive(self):
        filename = askopenfilename(filetypes=(
            ("Zip archive", "*.zip"),
            ("Zip archive", "*.ZIP"),
            ("Zip archive", "*.Zip")))
        if not filename:
            print("openfilename canceled...")
            return
        self._start_loading(filename)


class MainWindow(BaseHeatmapWindow):

    def __init__(self, master, controller, data_subject, profiles_subject):
        super(MainWindow, self).__init__(
            master, controller, data_subject, profiles_subject)

    def build_ui(self):
        self.build_base_ui()

        featuremat = FeaturesButton(
            self.main.button_ext, self.subject)
        featuremat.build_ui()

        sectors = SectorsButton(
            self.main.button_ext, self.subject)
        sectors.build_ui()

        open_buttons = OpenButtons(self.main.button_ext, self.subject)
        open_buttons.build_ui()

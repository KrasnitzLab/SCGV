'''
Created on Jan 17, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport

from utils.observer import Observer
from commands.open import OpenCommand
from commands.executor import CommandExecutor


class OpenUi(Observer):
    DELAY = 500

    def __init__(self, master, subject):
        super(OpenUi, self).__init__(subject)
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
        self.open_archive_button.config(state=tk.DISABLED)
        self.open_dir_button.config(state=tk.DISABLED)
        self.progress.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.progress.start()
        command = OpenCommand(self.master, self.subject, filename)
        CommandExecutor.execute(command)

    def _stop_loading(self):
        self.progress.stop()
        self.progress.grid_remove()

    def update(self):
        if self.get_model() is None:
            self._reset_loading()
        else:
            self._stop_loading()

    def _reset_loading(self):
        self.progress.stop()
        self.progress.grid_remove()
        self.open_archive_button.config(state=tk.ACTIVE)
        self.open_dir_button.config(state=tk.ACTIVE)

    def _open_archive(self):
        filename = askopenfilename(filetypes=(
            ("Zip archive", "*.zip"),
            ("Zip archive", "*.ZIP"),
            ("Zip archive", "*.Zip")))
        if not filename:
            print("openfilename canceled...")
            return
        self._start_loading(filename)

'''
Created on Jan 17, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport

import threading
import traceback


class OpenUi(object):
    DELAY = 500

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.model_lock = threading.RLock()
        self.model = None

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
        print("opening directory...")
        filename = askdirectory()
        if not filename:
            print("open directory canceled...")
            return
        print(filename)
        self.filename = filename
        self._start_loading()

    def _start_loading(self):
        self.open_archive_button.config(state=tk.DISABLED)
        self.open_dir_button.config(state=tk.DISABLED)
        self.loader_task = threading.Thread(target=self._loading, args=[self])
        self.loader_task.start()
        self.master.after(4 * self.DELAY, self._on_loading_progress, self)
        self.progress.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.progress.start()

    def _open_archive(self):
        print("opening archive...")
        filename = askopenfilename(filetypes=(
            ("Zip archive", "*.zip"),
            ("Zip archive", "*.ZIP"),
            ("Zip archive", "*.Zip")))
        if not filename:
            print("openfilename canceled...")
            return
        self.filename = filename
        self._start_loading()

    def _on_loading_progress(self, *args):
        if self.loader_task.is_alive():
            self.master.after(self.DELAY, self._on_loading_progress, self)
            return

        if not self.model_lock.acquire(False):
            return

        with self.model_lock:
            if self.model:
                self.progress.stop()
                self.progress.grid_remove()
                self.master.after(
                    self.DELAY,
                    self.controller.trigger_on_model_callbacks)

            else:
                self.progress.stop()
                self.progress.grid_remove()
                messagebox.showerror(
                    title="Wrong file/directory type",
                    message="Single Cell Genomics data set expected")

    def _loading(self, *args):
        with self.model_lock:
            try:
                print("loading '{}'".format(self.filename))
                self.model = self.controller.load_model(self.filename)
                return True
            except Exception:
                print("wrong dataset format")
                traceback.print_exc()
                self.model = None
                return False

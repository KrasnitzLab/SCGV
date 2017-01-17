'''
Created on Jan 16, 2017

@author: lubo
'''
import sys  # @UnusedImport
import threading

import matplotlib
matplotlib.use('TkAgg')


from utils.model import DataModel  # @IgnorePep8
from views.controller import MainController  # @IgnorePep8


# @IgnorePep8 @UnusedWildImport
from matplotlib.backends.backend_tkagg import *
from matplotlib.figure import Figure  # @IgnorePep8 @Reimport


if sys.version_info[0] < 3:
    import Tkinter as tk  # @UnusedImport @UnresolvedImport
    import ttk  # @UnusedImport @UnresolvedImport
    from tkFileDialog import askopenfilename  # @UnusedImport @UnresolvedImport
    import tkMessageBox as messagebox  # @UnusedImport @UnresolvedImport
else:
    import tkinter as tk  # @Reimport @UnresolvedImport
    from tkinter import ttk  # @UnresolvedImport @UnusedImport @Reimport
    from tkinter.filedialog \
        import askopenfilename  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter.filedialog \
        import askdirectory  # @UnresolvedImport @Reimport@UnusedImport

    from tkinter import messagebox  # @UnresolvedImport @Reimport @UnusedImport


class MainWindow(object):
    DELAY = 500

    def __init__(self, root):
        self.model_lock = threading.RLock()
        self.model = None
        self.loader_task = None
        self.filename = None

        self.root = root

        self.fig = Figure(figsize=(12, 8))

        self.content = tk.Frame(self.root)
        self.content.pack(side="top", fill="both", expand=True)

        self.canvas = FigureCanvasTkAgg(self.fig, self.content)
        self.canvas.show()

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.content)
        self.toolbar.update()

        self.toolbar_ext = ttk.Frame(
            self.content,
            # relief='sunken',
            borderwidth=5, width=150)
        self.button_ext = ttk.Frame(
            self.content, borderwidth=5, width=150)

        self.toolbar.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvas.get_tk_widget().grid(
            column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.toolbar_ext.grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.button_ext.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.content.columnconfigure(0, weight=99)
        self.content.rowconfigure(0, weight=0)
        self.content.columnconfigure(1, weight=0)
        self.content.rowconfigure(1, weight=99)

        self._build_button_ext()
        self._build_open_button()

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _build_button_ext(self):
        extframe = ttk.Frame(
            self.button_ext,
            # relief='sunken',
            borderwidth=5, width=150, height=100)
        extframe.grid(row=100, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.progress = ttk.Progressbar(
            self.button_ext, mode='indeterminate')

        self.quit_button = ttk.Button(
            master=self.button_ext,
            text='Quit',
            command=self._quit)
        self.quit_button.grid(row=1, column=0)

        self.button_ext.rowconfigure(100, weight=100)

    def _build_open_button(self):
        self.open_archive_button = ttk.Button(
            master=self.toolbar_ext,
            width=2,
            text="OA",
            command=self._open_archive)
        self.open_archive_button.grid(column=0, row=0)
        self.open_dir_button = ttk.Button(
            master=self.toolbar_ext,
            width=2,
            text="OD",
            command=self._open_dir)
        self.open_dir_button.grid(column=1, row=0)

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
        self.root.after(4 * self.DELAY, self._on_loading_progress, self)
        self.progress.grid(row=101, column=0, sticky=tk.W + tk.E + tk.N)
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
            self.root.after(self.DELAY, self._on_loading_progress, self)
            return

        if not self.model_lock.acquire(False):
            return

        with self.model_lock:
            if self.model:
                self.main = MainController(self.model)
                self.main.build_main(self.fig)
                self.canvas.draw()
                self.progress.stop()
                self.progress.grid_remove()
            else:
                self.progress.stop()
                self.progress.grid_remove()
                messagebox.showerror(
                    "Wrong file type",
                    "Single Cell Genomics ZIP archive expected")

    def _loading(self, *args):
        with self.model_lock:
            try:
                print("loading '{}'".format(self.filename))
                model = DataModel(self.filename)
                print("preparing '{}'".format(self.filename))
                model.make()
                self.model = model

                return True
            except AssertionError:
                print("wrong file type: ZIP archive expected")
                return False


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("cnviewer")

    main = MainWindow(root)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()

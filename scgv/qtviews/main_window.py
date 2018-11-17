import sys
import traceback

import numpy as np

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, \
    QStatusBar, QFileDialog, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot, \
    QThreadPool

from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from scgv.models.model import DataModel
from scgv.utils.observer import DataObserver


class WorkerSignals(QObject):

    finished = pyqtSignal()
    progress = pyqtSignal(int)

    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    status = pyqtSignal(object)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        print(self.args)
        print(self.kwargs)

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(
                *self.args, **self.kwargs,
                status=self.signals.status,
                progress=self.signals.progress,
            )
        except Exception:
            # Emit error
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            # Done
            self.signals.finished.emit()


class OpenButtons(object):

    def __init__(self, window, subject):
        # super(OpenButtons, self).__init__(subject)
        self.window = window

        self.window.toolbar.addSeparator()

        self.open_dir_action = QAction(
            QIcon("icons/folder.png"), "Open Directory", self.window)
        self.open_dir_action.setStatusTip("Open Directory button")
        self.open_dir_action.triggered.connect(self.on_open_directory_click)
        self.window.toolbar.addAction(self.open_dir_action)

        self.open_archive_action = QAction(
            QIcon("icons/archive.png"), "Open Archive", self.window)
        self.open_archive_action.setStatusTip("Open Archive button")
        self.open_archive_action.triggered.connect(self.on_open_archive_click)
        self.window.toolbar.addAction(self.open_archive_action)

        self.threadpool = QThreadPool()

    def on_open_directory_click(self, s):
        print("click open directory", s)
        dirname = QFileDialog.getExistingDirectory(
            self.window, "Open Directory")
        print(dirname)
        self._load_model(dirname)

    def on_open_archive_click(self, s):
        print("click open archive", s)
        filter = "Zip File (*.zip)"
        filename, _ = QFileDialog.getOpenFileName(
            self.window, "Open Zip File",
            ".", filter)
        print(filename)
        self._load_model(filename)

    def _load_model(self, filename):

        self.open_archive_action.setEnabled(False)
        self.open_dir_action.setEnabled(False)

        worker = Worker(self._build_model, filename)
        worker.signals.result.connect(self.window.set_model)
        worker.signals.error.connect(self._load_error)
        worker.signals.finished.connect(self._load_complete)
        self.threadpool.start(worker)

    def _load_complete(self):
        print("load complete")

    def _load_error(self, *args, **kwargs):
        print("_load_error: args=", args, "; kwargs=", kwargs)
        self.open_archive_action.setEnabled(True)
        self.open_dir_action.setEnabled(True)

    def _build_model(self, filename, *args, **kwargs):
            print("_build_model: args=", args, "; kwargs=", kwargs)
            model = DataModel(filename)
            model.make()
            return model


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("SCGV Main")

        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(static_canvas)

        self.toolbar = NavigationToolbar(static_canvas, self)
        self.addToolBar(self.toolbar)

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self.setStatusBar(QStatusBar(self))
        self.open_buttons = OpenButtons(self, None)

    def set_model(self, model):
        print("set model:", model)

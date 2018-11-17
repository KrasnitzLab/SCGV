import numpy as np

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, \
    QStatusBar
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


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

        self.toolbar.addSeparator()

        open_dir_action = QAction(
            QIcon("icons/folder.png"), "Open Directory", self)
        open_dir_action.setStatusTip("Open Directory button")
        open_dir_action.triggered.connect(self.on_open_directory_click)
        self.toolbar.addAction(open_dir_action)

        open_archive_action = QAction(
            QIcon("icons/archive.png"), "Open Archive", self)
        open_archive_action.setStatusTip("Open Archive button")
        open_archive_action.triggered.connect(self.on_open_archive_click)
        self.toolbar.addAction(open_archive_action)

    def on_open_directory_click(self, s):
        print("click open directory", s)        
    
    def on_open_archive_click(self, s):
        print("click open archive", s)
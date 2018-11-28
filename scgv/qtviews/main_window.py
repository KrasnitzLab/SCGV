import sys
import traceback

import os
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, \
    QStatusBar, QFileDialog, \
    QHBoxLayout, QVBoxLayout, \
    QListWidget, QListWidgetItem, \
    QPushButton, QDialog, QMenu, QLabel, \
    QTextEdit

from PyQt5.QtGui import QIcon, QPixmap, QImage, QTextDocument
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot, \
    QThreadPool, Qt

from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PIL import ImageQt, Image

from scgv.models.model import DataModel
from scgv.utils.observer import DataObserver

import matplotlib.pyplot as plt
import matplotlib.colors as col

from scgv.views.clone import CloneViewer
from scgv.views.heatmap import HeatmapViewer
from scgv.views.sector import SectorViewer
from scgv.views.gate import GateViewer
from scgv.views.multiplier import MultiplierViewer
from scgv.views.error import ErrorViewer
from scgv.views.dendrogram import DendrogramViewer
from scgv.views.sample import SamplesViewer

from scgv.utils.color_map import ColorMap


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


def icons_folder():
    modulename = os.path.abspath(__file__)
    dirname = os.path.dirname(modulename)
    iconsdir = os.path.join(dirname, 'icons')
    return iconsdir


class OpenButtons(object):

    def __init__(self, window, subject):
        # super(OpenButtons, self).__init__(subject)
        self.window = window

        self.window.toolbar.addSeparator()
        icons = icons_folder()

        self.open_dir_action = QAction(
            QIcon(os.path.join(icons, "folder.png")), 
            "Open Directory", self.window)
        self.open_dir_action.setStatusTip("Open Directory button")
        self.open_dir_action.triggered.connect(self.on_open_directory_click)
        self.window.toolbar.addAction(self.open_dir_action)

        self.open_archive_action = QAction(
            QIcon(os.path.join(icons, "archive.png")), 
            "Open Archive", self.window)
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
        self.window.update()
        print("window updated called...")

    def _load_error(self, *args, **kwargs):
        print("_load_error: args=", args, "; kwargs=", kwargs)
        self.open_archive_action.setEnabled(True)
        self.open_dir_action.setEnabled(True)

    def _build_model(self, filename, *args, **kwargs):
            print("_build_model: args=", args, "; kwargs=", kwargs)
            model = DataModel(filename)
            model.make()
            return model


class CanvasSignals(QObject):
    profile_selected = pyqtSignal(object)


class Canvas(FigureCanvas):

    W = 0.8875
    X = 0.075

    def __init__(self):
        self.fig = Figure(figsize=(12, 8))
        self.model = None
        super(Canvas, self).__init__(self.fig)
        self.signals = CanvasSignals()
        self.cid = None

    def draw_canvas(self):
        assert self.model is not None

        ax_dendro = self.fig.add_axes(
            [self.X, 0.775, self.W, 0.175], frame_on=True)
        dendro_viewer = DendrogramViewer(self.model)
        dendro_viewer.draw_dendrogram(ax_dendro)

        ax_clone = self.fig.add_axes(
            [self.X, 0.7625, self.W, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer = CloneViewer(self.model)
        clone_viewer.draw_clone(ax_clone)
        ax_subclone = self.fig.add_axes(
            [self.X, 0.75, self.W, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer.draw_subclone(ax_subclone)

        ax_heat = self.fig.add_axes(
            [self.X, 0.20, self.W, 0.55], frame_on=True, sharex=ax_dendro)

        heatmap_viewer = HeatmapViewer(self.model)
        heatmap_viewer.draw_heatmap(ax_heat)

        ax_sector = self.fig.add_axes(
            [self.X, 0.175, self.W, 0.025], frame_on=True, sharex=ax_dendro)
        # draw sector bar
        sector_viewer = SectorViewer(self.model)
        sector_viewer.draw_sector(ax_sector)

        ax_gate = self.fig.add_axes(
            [self.X, 0.150, self.W, 0.025], frame_on=True, sharex=ax_dendro)
        gate_viewer = GateViewer(self.model)
        gate_viewer.draw_ploidy(ax_gate)

        ax_multiplier = self.fig.add_axes(
            [self.X, 0.125, self.W, 0.025], frame_on=True, sharex=ax_dendro)
        multiplier_viewer = MultiplierViewer(self.model)
        multiplier_viewer.draw_multiplier(ax_multiplier)

        ax_error = self.fig.add_axes(
            [self.X, 0.10, self.W, 0.025], frame_on=True, sharex=ax_dendro)
        error_viewer = ErrorViewer(self.model)
        error_viewer.draw_error(ax_error)
        error_viewer.draw_xlabels(ax_error)

        self.ax_label = ax_error

        plt.setp(ax_dendro.get_xticklabels(), visible=False)
        plt.setp(ax_clone.get_xticklabels(), visible=False)
        plt.setp(ax_clone.get_xticklines(), visible=False)
        plt.setp(ax_subclone.get_xticklabels(), visible=False)
        plt.setp(ax_subclone.get_xticklines(), visible=False)
        plt.setp(ax_heat.get_xticklabels(), visible=False)
        plt.setp(ax_sector.get_xticklabels(), visible=False)
        plt.setp(ax_gate.get_xticklabels(), visible=False)
        plt.setp(ax_multiplier.get_xticklabels(), visible=False)

    def redraw(self):
        if self.model is not None:
            self.draw_canvas()
            self.draw()

    def onclick(self, event):
        print(
            '%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            ('double' if event.dblclick else 'single', event.button,
             event.x, event.y, event.xdata, event.ydata))
        if event.button == 3:
            sample_name = self.locate_sample_click(event)
            print("Located sample:", sample_name)
            self.signals.profile_selected.emit(sample_name)

    def set_model(self, model):
        print("Canvas: set model:", model)
        self.model = model
        if self.model is not None and self.cid is None:
            self.cid = self.fig.canvas.mpl_connect(
                "button_press_event", self.onclick)

    def locate_sample_click(self, event):
        if event.xdata is None:
            return None
        xloc = int(event.xdata / self.model.interval_length)
        sample_name = self.model.column_labels[xloc]
        return sample_name

    def on_profile_selected(self, *args, **kwargs):
        print("canvas.on_profile_selected():", args, kwargs)


class ShowProfilesWindow(QDialog):

    def __init__(self, model, profiles, parent, *args, **kwargs):
        super(ShowProfilesWindow, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("SCGV Show Profiles")

        self._main = QWidget(self)
        layout = QVBoxLayout(self)

        self.fig = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.fig)

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.model = model
        self.profiles = profiles

        self.draw_canvas()
        self.canvas.draw()

    def draw_canvas(self):
        samples_viewer = SamplesViewer(self.model)
        samples_viewer.draw_samples(self.fig, self.profiles)


class ShowPathologyWindow(QDialog):

    def __init__(self, image, notes, parent, *args, **kwargs):
        super(ShowPathologyWindow, self).__init__(parent, *args, **kwargs)
        self.image = QImage(ImageQt.ImageQt(image))
        self.notes = notes

        label = QLabel(self)
        pixmap = QPixmap(self.image)
        label.setPixmap(pixmap)

        text = QTextEdit(self)
        text.setReadOnly(True)

        doc = QTextDocument()
        doc.setPlainText("".join(notes))
        text.setDocument(doc)

        layout = QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(text)


class LegendWidget(QWidget):
    IMAGE_SIZE = 15

    def __init__(self, main, *args, **kwargs):
        super(LegendWidget, self).__init__(*args, **kwargs)
        self.main = main

        layout = QVBoxLayout(self)
        self.list = QListWidget(self)
        layout.addWidget(self.list)

    @staticmethod
    def color255(color):
        c = col.to_rgba(color)
        if len(c) == 3:
            r, g, b = color
            a = 1
        elif len(c) == 4:
            r, g, b, a = color
        else:
            raise ValueError("strange color: {}".format(str(color)))
        return (int(255 * r), int(255 * g), int(255 * b), int(255 * a))

    def color_icon(self, color):
        image = Image.new(
            'RGBA',
            size=(self.IMAGE_SIZE, self.IMAGE_SIZE),
            color=self.color255(color))
        qimage = QImage(ImageQt.ImageQt(image))
        return QIcon(QPixmap(qimage))

    def add_entry(self, text, color):
        icon = self.color_icon(color)

        item = QListWidgetItem(icon, text, self.list)
        self.list.addItem(item)

    def show(self):
        raise NotImplementedError()

    def set_model(self, model):
        self.model = model
        self.show()


class HeatmapLegend(LegendWidget):

    COPYNUM_LABELS = [
        "    0", "    1", "    2", "    3", "    4+"
    ]

    def __init__(self, main, *args, **kwargs):
        super(HeatmapLegend, self).__init__(main, *args, **kwargs)

    def show(self):
        cmap = ColorMap.make_diverging05()
        for index, label in enumerate(self.COPYNUM_LABELS):
            color = cmap.colors(index)
            self.add_entry(label, color)


class SectorsLegend(LegendWidget):

    def __init__(self, main, *args, **kwargs):
        super(SectorsLegend, self).__init__(main, *args, **kwargs)
        self.sectors = None

    def show(self):
        assert self.model is not None

        if self.sectors is None:
            self.sectors = self.model.make_sectors_legend()
        if self.sectors is None:
            return

        self.cmap = ColorMap.make_qualitative12()

        for (index, (sector, pathology)) in enumerate(self.sectors):
            color = self.cmap.colors(index)
            self.add_entry(
                text=pathology,
                color=color)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, pos, *args, **kwargs):
        print("SectorsLegend.on_context_menu()", args, kwargs)
        print(self.list.currentRow())

        show_sector_view = QAction("Show sector view", self)
        show_sector_view.triggered.connect(self.show_sector_view)
        show_pathology_view = QAction("Show sector pathology", self)
        show_pathology_view.triggered.connect(self.show_pathology_view)

        context = QMenu(self)
        context.addAction(show_sector_view)
        if self.model.pathology:
            context.addAction(show_pathology_view)
        context.exec_(self.mapToGlobal(pos))

    def show_sector_view(self):
        print("SectorsLegend.show_sector_view()")
        print(self.list.currentRow())

    def show_pathology_view(self):
        print("SectorsLegend.show_pathology_view()")
        print(self.list.currentRow())
        print(self.list.currentItem().text())
        print(self.model.pathology)

        if self.model.pathology is None:
            return

        pathology = self.list.currentItem().text()
        image, notes = self.model.pathology.get(pathology, (None, None))

        dialog = ShowPathologyWindow(image, notes, self.main)
        dialog.show()


class ProfilesWidget(QWidget):

    def __init__(self, main, *args, **kwargs):
        super(ProfilesWidget, self).__init__(*args, **kwargs)
        self.main = main

        self.profiles = []
        layout = QVBoxLayout(self)
        self.profiles_list = QListWidget(self)
        layout.addWidget(self.profiles_list)
        self.profiles_show_button = QPushButton("Profiles Show")
        self.profiles_show_button.clicked.connect(
            self.on_profiles_show
        )
        layout.addWidget(self.profiles_show_button)

        self.profiles_clear_button = QPushButton("Profiles Clear")
        self.profiles_clear_button.clicked.connect(
            self.on_profiles_clear
        )
        layout.addWidget(self.profiles_clear_button)

        self.model = None

    def set_model(self, model):
        self.model = model

    def on_profile_selected(self, profile, *args, **kwargs):
        if profile in self.profiles:
            return
        self.profiles_list.addItem(profile)
        self.profiles.append(profile)

    def on_profiles_clear(self, *args, **kwargs):
        self.profiles_list.clear()
        self.profiles = []

    def on_profiles_show(self, *args, **kwargs):
        if not self.profiles:
            return
        profiles = self.profiles[:]
        self.profiles_list.clear()
        self.profiles = []

        show_profiles = ShowProfilesWindow(
            self.model, profiles, self.main
        )
        show_profiles.show()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("SCGV Main")

        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QHBoxLayout(self._main)

        self.canvas = Canvas()
        layout.addWidget(self.canvas, stretch=1)

        self.commands_pane = QVBoxLayout(self._main)
        layout.addLayout(self.commands_pane)

        self.profiles = ProfilesWidget(self)
        self.commands_pane.addWidget(self.profiles, stretch=0)

        self.heatmap_legend = HeatmapLegend(self)
        self.commands_pane.addWidget(self.heatmap_legend)

        self.sectors_legend = SectorsLegend(self)
        self.commands_pane.addWidget(self.sectors_legend)

        self.commands_pane.addStretch(1)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.addToolBar(self.toolbar)

        self.setStatusBar(QStatusBar(self))
        self.open_buttons = OpenButtons(self, None)

        self.connect_profile_actions()

    def connect_profile_actions(self):
        self.canvas.signals.profile_selected.connect(
            self.profiles.on_profile_selected)
        self.canvas.signals.profile_selected.connect(
            self.profiles.on_profile_selected)

    def set_model(self, model):
        print("set model:", model)
        self.model = model
        self.canvas.set_model(model)
        self.profiles.set_model(model)
        self.heatmap_legend.set_model(model)
        self.sectors_legend.set_model(model)

    def update(self):
        if self.model is not None:
            self.canvas.redraw()
        super(MainWindow, self).update()


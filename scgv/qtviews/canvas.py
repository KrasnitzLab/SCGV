from PyQt5.QtCore import QObject, pyqtSignal

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas

import matplotlib.pyplot as plt

from scgv.views.clone import CloneViewer
from scgv.views.heatmap import HeatmapViewer
from scgv.views.sector import SectorViewer
from scgv.views.gate import GateViewer
from scgv.views.multiplier import MultiplierViewer
from scgv.views.error import ErrorViewer
from scgv.views.dendrogram import DendrogramViewer


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
        # print(
        #     '%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #     ('double' if event.dblclick else 'single', event.button,
        #      event.x, event.y, event.xdata, event.ydata))
        if event.button == 3:
            sample_name = self.locate_sample_click(event)
            # print("Located sample:", sample_name)
            self.signals.profile_selected.emit(sample_name)

    def set_model(self, model):
        # print("Canvas: set model:", model)
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
        # print("canvas.on_profile_selected():", args, kwargs)
        pass


class SectorsCanvas(Canvas):

    def __init__(self):
        super(SectorsCanvas, self).__init__()

    def draw_canvas(self):
        assert self.model is not None

        ax_clone = self.fig.add_axes(
            [self.X, 0.9375, self.W, 0.0125], frame_on=True)
        clone_viewer = CloneViewer(self.model)
        clone_viewer.draw_clone(ax_clone)
        ax_subclone = self.fig.add_axes(
            [self.X, 0.925, self.W, 0.0125], frame_on=True, sharex=ax_clone)
        clone_viewer.draw_subclone(ax_subclone)

        ax_heat = self.fig.add_axes(
            [self.X, 0.20, self.W, 0.725], frame_on=True, sharex=ax_clone)
        featuremat_viewer = HeatmapViewer(self.model)
        featuremat_viewer.draw_heatmap(ax_heat)

        ax_sector = self.fig.add_axes(
            [self.X, 0.175, self.W, 0.025], frame_on=True, sharex=ax_clone)
        # draw sector bar
        sector_viewer = SectorViewer(self.model)
        sector_viewer.draw_sector(ax_sector)

        ax_gate = self.fig.add_axes(
            [self.X, 0.150, self.W, 0.025], frame_on=True, sharex=ax_clone)
        gate_viewer = GateViewer(self.model)
        gate_viewer.draw_ploidy(ax_gate)

        ax_multiplier = self.fig.add_axes(
            [self.X, 0.125, self.W, 0.025], frame_on=True, sharex=ax_clone)
        multiplier_viewer = MultiplierViewer(self.model)
        multiplier_viewer.draw_multiplier(ax_multiplier)

        ax_error = self.fig.add_axes(
            [self.X, 0.10, self.W, 0.025], frame_on=True, sharex=ax_clone)
        error_viewer = ErrorViewer(self.model)
        error_viewer.draw_error(ax_error)
        error_viewer.draw_xlabels(ax_error)
        self.ax_label = ax_error

        plt.setp(ax_clone.get_xticklabels(), visible=False)
        plt.setp(ax_subclone.get_xticklabels(), visible=False)

        plt.setp(ax_heat.get_xticklabels(), visible=False)
        plt.setp(ax_sector.get_xticklabels(), visible=False)
        plt.setp(ax_gate.get_xticklabels(), visible=False)
        plt.setp(ax_multiplier.get_xticklabels(), visible=False)

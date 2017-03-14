'''
Created on Feb 22, 2017

@author: lubo
'''
import matplotlib.pyplot as plt

from tkviews.base_window import BaseHeatmapWindow
from views.clone import CloneViewer
from views.heatmap import HeatmapViewer
from views.sector import SectorViewer
from views.gate import GateViewer
from views.multiplier import MultiplierViewer
from views.error import ErrorViewer


class SectorsWindow(BaseHeatmapWindow):

    def __init__(self, master, controller, subject):
        super(SectorsWindow, self).__init__(master, controller, subject)
        assert controller.model is not None

    def draw_canvas(self):
        assert self.controller.model is not None
        self.model = self.controller.model

        ax_clone = self.fig.add_axes(
            [0.1, 0.9375, 0.8, 0.0125], frame_on=True)
        clone_viewer = CloneViewer(self.model)
        clone_viewer.draw_clone(ax_clone)
        ax_subclone = self.fig.add_axes(
            [0.1, 0.925, 0.8, 0.0125], frame_on=True, sharex=ax_clone)
        clone_viewer.draw_subclone(ax_subclone)

        ax_heat = self.fig.add_axes(
            [0.1, 0.20, 0.8, 0.725], frame_on=True, sharex=ax_clone)
        pinmat_viewer = HeatmapViewer(self.model)
        pinmat_viewer.draw_heatmap(ax_heat)

        ax_sector = self.fig.add_axes(
            [0.1, 0.175, 0.8, 0.025], frame_on=True, sharex=ax_clone)
        # draw sector bar
        sector_viewer = SectorViewer(self.model)
        sector_viewer.draw_sector(ax_sector)

        ax_gate = self.fig.add_axes(
            [0.1, 0.150, 0.8, 0.025], frame_on=True, sharex=ax_clone)
        gate_viewer = GateViewer(self.model)
        gate_viewer.draw_ploidy(ax_gate)

        ax_multiplier = self.fig.add_axes(
            [0.1, 0.125, 0.8, 0.025], frame_on=True, sharex=ax_clone)
        multiplier_viewer = MultiplierViewer(self.model)
        multiplier_viewer.draw_multiplier(ax_multiplier)

        ax_error = self.fig.add_axes(
            [0.1, 0.10, 0.8, 0.025], frame_on=True, sharex=ax_clone)
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

        self.controller.event_loop_connect(self.fig)

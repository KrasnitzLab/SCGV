'''
Created on Feb 21, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport
from tkutils.canvas_ui import CanvasWindow
import matplotlib.pyplot as plt


from tkutils.profiles_ui import ProfilesUi
from tkutils.sectors_legend2 import SectorsLegend2
from tkutils.heatmap_legend import HeatmapLegend
from tkutils.sectors_ui import SectorsUi

from views.dendrogram import DendrogramViewer
from views.clone import CloneViewer
from views.sector import SectorViewer
from views.gate import GateViewer
from views.multiplier import MultiplierViewer
from views.error import ErrorViewer
from views.sample import SampleViewer
from views.pinmat import PinmatViewer


class PinmatWindow(object):

    def __init__(self, master, controller):
        assert controller.model is not None
        self.master = master
        self.controller = controller

    def build_ui(self):
        self.main = CanvasWindow(self.master, self.controller)
        self.fig = self.main.fig

        profiles = ProfilesUi(self.main.button_ext, self.main)
        profiles.build_ui()

        sectors = SectorsUi(self.main.button_ext)
        sectors.build_ui()

        sectors_legend = SectorsLegend2(self.main.legend_ext)
        sectors_legend.build_ui(row=10)
        # sectors_legend.register_show_single_sector_callback(show_single_sector)

        heatmap_legend = HeatmapLegend(self.main.legend_ext)
        heatmap_legend.build_ui()
        heatmap_legend.show_legend()

    def register_on_closing_callback(self, cb):
        self.main.register_on_closing_callback(cb)

    def draw_canvas(self):
        assert self.controller.model is not None
        self.model = self.controller.model

        ax_dendro = self.fig.add_axes([0.1, 0.775, 0.8, 0.175], frame_on=True)
        dendro_viewer = DendrogramViewer(self.model)
        dendro_viewer.draw_dendrogram(ax_dendro)

        ax_clone = self.fig.add_axes(
            [0.1, 0.7625, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer = CloneViewer(self.model)
        clone_viewer.draw_clone(ax_clone)
        ax_subclone = self.fig.add_axes(
            [0.1, 0.75, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer.draw_subclone(ax_subclone)

        ax_heat = self.fig.add_axes(
            [0.1, 0.20, 0.8, 0.55], frame_on=True, sharex=ax_dendro)
        pinmat_viewer = PinmatViewer(self.model)
        pinmat_viewer.draw_heatmap(ax_heat)

        ax_sector = self.fig.add_axes(
            [0.1, 0.175, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        # draw sector bar
        sector_viewer = SectorViewer(self.model)
        sector_viewer.draw_sector(ax_sector)

        ax_gate = self.fig.add_axes(
            [0.1, 0.150, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        gate_viewer = GateViewer(self.model)
        gate_viewer.draw_ploidy(ax_gate)

        ax_multiplier = self.fig.add_axes(
            [0.1, 0.125, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        multiplier_viewer = MultiplierViewer(self.model)
        multiplier_viewer.draw_multiplier(ax_multiplier)

        ax_error = self.fig.add_axes(
            [0.1, 0.10, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
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

        self.sample_viewer = SampleViewer(self.model)
        self.controller.event_loop_connect(self.fig)

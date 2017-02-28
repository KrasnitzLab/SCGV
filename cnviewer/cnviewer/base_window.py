'''
Created on Feb 21, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport

from tkutils.canvas_ui import CanvasWindow
from tkutils.profiles_ui import ProfilesUi
from tkutils.sectors_legend2 import SectorsLegend2
from tkutils.heatmap_legend import HeatmapLegend
from cnviewer.samples_window import SamplesWindow
from controllers.controller import SamplesController, SingleSectorController

import numpy as np
from models.sector_model import SingleSectorDataModel

import matplotlib.pyplot as plt

from views.clone import CloneViewer
from views.heatmap import HeatmapViewer
from views.sector import SectorViewer
from views.gate import GateViewer
from views.multiplier import MultiplierViewer
from views.error import ErrorViewer
import traceback


class BaseHeatmapWindow(object):

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.controller.register_sample_cb(
            self.highlight_profiles_labels,
            self.unhighlight_profile_labels,
            self.build_sample_window
        )
        self.ax_label = None

    def refresh(self):
        self.main.refresh()

    def register_on_closing_callback(self, cb):
        self.main.register_on_closing_callback(cb)

    def build_ui(self):
        self.build_base_ui()

    def build_base_ui(self):
        self.main = CanvasWindow(self.master, self.controller)
        self.fig = self.main.fig

        profiles = ProfilesUi(self.main.button_ext, self.controller)
        profiles.build_ui()

        sectors_legend = SectorsLegend2(self.main.legend_ext, self.controller)
        sectors_legend.build_ui(row=10)
        sectors_legend.register_show_single_sector_callback(
            self.build_single_sector_window)

        heatmap_legend = HeatmapLegend(self.main.legend_ext, self.controller)
        heatmap_legend.build_ui(row=20)
        heatmap_legend.show_legend()

    def build_sample_window(self, samples):
        print("build_sample_window called... showing: {}".format(samples))
        root = tk.Toplevel()
        controller = SamplesController(self.controller.model)
        samples_window = SamplesWindow(root, controller, samples)
        samples_window.build_ui()
        samples_window.draw_canvas()
        root.mainloop()

    def build_single_sector_window(self, model, sector_id):
        try:
            sector_model = SingleSectorDataModel(model, sector_id)
            sector_model.make()

            controller = SingleSectorController(sector_model)

            root = tk.Toplevel()
            main = SingleSectorWindow(root, controller)
            main.build_ui()
            main.draw_canvas()

            root.mainloop()
        except Exception:
            traceback.print_exc()

    def get_profile_indices(self, profiles):
        profile_indices = []
        for i, p in enumerate(self.model.column_labels):
            if p in profiles:
                profile_indices.append(i)

        profile_indices = np.array(profile_indices)
        return profile_indices

    def highlight_profiles_labels(self, profiles):
        if self.ax_label is None:
            return
        profile_indices = self.get_profile_indices(profiles)
        print("highlight profiles: {}".format(profile_indices))
        for index in profile_indices:
            self.ax_label.get_xticklabels()[index].set_color('red')
        self.refresh()

    def unhighlight_profile_labels(self, profiles):
        if self.ax_label is None:
            return
        profile_indices = self.get_profile_indices(profiles)
        print("unhighlight profiles: {}".format(profile_indices))
        for index in profile_indices:
            self.ax_label.get_xticklabels()[index].set_color('black')
        self.refresh()


class SingleSectorWindow(BaseHeatmapWindow):

    def __init__(self, master, controller):
        super(SingleSectorWindow, self).__init__(master, controller)

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

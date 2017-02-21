'''
Created on Dec 14, 2016

@author: lubo
'''
import matplotlib.pyplot as plt
import numpy as np

from views.sample import SampleViewer
from views.heatmap import HeatmapViewer
from views.clone import CloneViewer
from views.gate import GateViewer
from views.multiplier import MultiplierViewer
from views.error import ErrorViewer
from views.sector import SectorViewer
from controllers.controller_base import ControllerBase
from models.model import DataModel


class PinmatController(ControllerBase):

    def __init__(self, model):
        super(PinmatController, self).__init__()
        self.model = model


class MainController(ControllerBase):

    def __init__(self):
        super(MainController, self).__init__()
        self.sample_viewer = None
        self.model = None
        self.on_model_callbacks = []

        self.add_sample_cb = None
        self.ax_label = None

    def register_on_model_callback(self, cb):
        self.on_model_callbacks.append(cb)

    def load_model(self, filename):
        self.filename = filename
        self.model = DataModel(self.filename)
        self.model.make()
        return self.model

    def trigger_on_model_callbacks(self):
        for cb in self.on_model_callbacks:
            cb(self.model)
        return self.model

#     def build_main(self, fig):
#         assert self.fig is None
#         self.fig = fig
#
#         ax_dendro = fig.add_axes([0.1, 0.775, 0.8, 0.175], frame_on=True)
#         dendro_viewer = DendrogramViewer(self.model)
#         dendro_viewer.draw_dendrogram(ax_dendro)
#
#         ax_clone = fig.add_axes(
#             [0.1, 0.7625, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
#         clone_viewer = CloneViewer(self.model)
#         clone_viewer.draw_clone(ax_clone)
#         ax_subclone = fig.add_axes(
#             [0.1, 0.75, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
#         clone_viewer.draw_subclone(ax_subclone)
#
#         ax_heat = fig.add_axes(
#             [0.1, 0.20, 0.8, 0.55], frame_on=True, sharex=ax_dendro)
#
#         heatmap_viewer = HeatmapViewer(self.model)
#         heatmap_viewer.draw_heatmap(ax_heat)
#         # heatmap_viewer.draw_legend()
#
#         ax_sector = fig.add_axes(
#             [0.1, 0.175, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
#         # draw sector bar
#         sector_viewer = SectorViewer(self.model)
#         sector_viewer.draw_sector(ax_sector)
#
#         ax_gate = fig.add_axes(
#             [0.1, 0.150, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
#         gate_viewer = GateViewer(self.model)
#         gate_viewer.draw_ploidy(ax_gate)
#
#         ax_multiplier = fig.add_axes(
#             [0.1, 0.125, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
#         multiplier_viewer = MultiplierViewer(self.model)
#         multiplier_viewer.draw_multiplier(ax_multiplier)
#
#         ax_error = fig.add_axes(
#             [0.1, 0.10, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
#         error_viewer = ErrorViewer(self.model)
#         error_viewer.draw_error(ax_error)
#         error_viewer.draw_xlabels(ax_error)
#
#         self.ax_label = ax_error
#
#         plt.setp(ax_dendro.get_xticklabels(), visible=False)
#         plt.setp(ax_clone.get_xticklabels(), visible=False)
#         plt.setp(ax_clone.get_xticklines(), visible=False)
#         plt.setp(ax_subclone.get_xticklabels(), visible=False)
#         plt.setp(ax_subclone.get_xticklines(), visible=False)
#         plt.setp(ax_heat.get_xticklabels(), visible=False)
#         plt.setp(ax_sector.get_xticklabels(), visible=False)
#         plt.setp(ax_gate.get_xticklabels(), visible=False)
#         plt.setp(ax_multiplier.get_xticklabels(), visible=False)
#
#         self.sample_viewer = SampleViewer(self.model)
#         self.event_loop_connect()

#     def build_pinmat(self, fig):
#         assert self.fig is None
#         self.fig = fig
#
#         ax_dendro = fig.add_axes([0.1, 0.775, 0.8, 0.175], frame_on=True)
#         dendro_viewer = DendrogramViewer(self.model)
#         dendro_viewer.draw_dendrogram(ax_dendro)
#
#         ax_clone = fig.add_axes(
#             [0.1, 0.7625, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
#         clone_viewer = CloneViewer(self.model)
#         clone_viewer.draw_clone(ax_clone)
#         ax_subclone = fig.add_axes(
#             [0.1, 0.75, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
#         clone_viewer.draw_subclone(ax_subclone)
#
#         ax_heat = fig.add_axes(
#             [0.1, 0.20, 0.8, 0.55], frame_on=True, sharex=ax_dendro)
#         pinmat_viewer = PinmatViewer(self.model)
#         pinmat_viewer.draw_heatmap(ax_heat)
#
#         ax_sector = fig.add_axes(
#             [0.1, 0.175, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
#         # draw sector bar
#         sector_viewer = SectorViewer(self.model)
#         sector_viewer.draw_sector(ax_sector)
#
#         ax_gate = fig.add_axes(
#             [0.1, 0.150, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
#         gate_viewer = GateViewer(self.model)
#         gate_viewer.draw_ploidy(ax_gate)
#
#         ax_multiplier = fig.add_axes(
#             [0.1, 0.125, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
#         multiplier_viewer = MultiplierViewer(self.model)
#         multiplier_viewer.draw_multiplier(ax_multiplier)
#
#         ax_error = fig.add_axes(
#             [0.1, 0.10, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
#         error_viewer = ErrorViewer(self.model)
#         error_viewer.draw_error(ax_error)
#         error_viewer.draw_xlabels(ax_error)
#         self.ax_label = ax_error
#
#         plt.setp(ax_dendro.get_xticklabels(), visible=False)
#         plt.setp(ax_clone.get_xticklabels(), visible=False)
#         plt.setp(ax_clone.get_xticklines(), visible=False)
#         plt.setp(ax_subclone.get_xticklabels(), visible=False)
#         plt.setp(ax_subclone.get_xticklines(), visible=False)
#         plt.setp(ax_heat.get_xticklabels(), visible=False)
#         plt.setp(ax_sector.get_xticklabels(), visible=False)
#         plt.setp(ax_gate.get_xticklabels(), visible=False)
#         plt.setp(ax_multiplier.get_xticklabels(), visible=False)
#
#         self.sample_viewer = SampleViewer(self.model)
#         self.event_loop_connect()

    def build_sector(self, fig):
        assert self.fig is None
        self.fig = fig

        ax_clone = fig.add_axes(
            [0.1, 0.9375, 0.8, 0.0125], frame_on=True)
        clone_viewer = CloneViewer(self.model)
        clone_viewer.draw_clone(ax_clone)
        ax_subclone = fig.add_axes(
            [0.1, 0.925, 0.8, 0.0125], frame_on=True, sharex=ax_clone)
        clone_viewer.draw_subclone(ax_subclone)

        ax_heat = fig.add_axes(
            [0.1, 0.20, 0.8, 0.725], frame_on=True, sharex=ax_clone)
        pinmat_viewer = HeatmapViewer(self.model)
        pinmat_viewer.draw_heatmap(ax_heat)

        ax_sector = fig.add_axes(
            [0.1, 0.175, 0.8, 0.025], frame_on=True, sharex=ax_clone)
        # draw sector bar
        sector_viewer = SectorViewer(self.model)
        sector_viewer.draw_sector(ax_sector)

        ax_gate = fig.add_axes(
            [0.1, 0.150, 0.8, 0.025], frame_on=True, sharex=ax_clone)
        gate_viewer = GateViewer(self.model)
        gate_viewer.draw_ploidy(ax_gate)

        ax_multiplier = fig.add_axes(
            [0.1, 0.125, 0.8, 0.025], frame_on=True, sharex=ax_clone)
        multiplier_viewer = MultiplierViewer(self.model)
        multiplier_viewer.draw_multiplier(ax_multiplier)

        ax_error = fig.add_axes(
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

        self.sample_viewer = SampleViewer(self.model)
        self.event_loop_connect()

    def get_profile_indices(self, profiles):
        profile_indices = []
        for i, p in enumerate(self.model.column_labels):
            if p in profiles:
                profile_indices.append(i)

        profile_indices = np.array(profile_indices)
        return profile_indices

    def highlight_profiles_labels(self, profiles):
        profile_indices = self.get_profile_indices(profiles)
        print("highlight profiles: {}".format(profile_indices))
        for index in profile_indices:
            self.ax_label.get_xticklabels()[index].set_color('red')

    def unhighlight_profile_labels(self, profiles):
        profile_indices = self.get_profile_indices(profiles)
        print("unhighlight profiles: {}".format(profile_indices))
        for index in profile_indices:
            self.ax_label.get_xticklabels()[index].set_color('black')

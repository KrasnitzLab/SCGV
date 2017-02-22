'''
Created on Feb 21, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport

from tkutils.canvas_ui import CanvasWindow
from tkutils.profiles_ui import ProfilesUi
from tkutils.sectors_legend2 import SectorsLegend2
from tkutils.heatmap_legend import HeatmapLegend
from cnviewer.sample_window import SamplesWindow
from controllers.controller import SamplesController

import numpy as np


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

    def build_base_ui(self):
        self.main = CanvasWindow(self.master, self.controller)
        self.fig = self.main.fig

        profiles = ProfilesUi(self.main.button_ext, self.controller)
        profiles.build_ui()

        sectors_legend = SectorsLegend2(self.main.legend_ext)
        sectors_legend.build_ui(row=10)
        # sectors_legend.register_show_single_sector_callback(show_single_sector)

        heatmap_legend = HeatmapLegend(self.main.legend_ext)
        heatmap_legend.build_ui()
        heatmap_legend.show_legend()

    def build_sample_window(self, samples):
        print("build_sample_window called... showing: {}".format(samples))
        root = tk.Toplevel()
        controller = SamplesController(self.controller.model)
        samples_window = SamplesWindow(root, controller, samples)
        samples_window.build_ui()
        samples_window.draw_canvas()
        root.mainloop()

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

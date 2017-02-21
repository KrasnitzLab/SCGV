'''
Created on Feb 21, 2017

@author: lubo
'''
from tkutils.canvas_ui import CanvasWindow
from tkutils.profiles_ui import ProfilesUi
from tkutils.sectors_legend2 import SectorsLegend2
from tkutils.heatmap_legend import HeatmapLegend


class BaseHeatmapWindow(object):

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

    def build_base_ui(self):
        self.main = CanvasWindow(self.master, self.controller)
        self.fig = self.main.fig

        profiles = ProfilesUi(self.main.button_ext, self.main)
        profiles.build_ui()

        sectors_legend = SectorsLegend2(self.main.legend_ext)
        sectors_legend.build_ui(row=10)
        # sectors_legend.register_show_single_sector_callback(show_single_sector)

        heatmap_legend = HeatmapLegend(self.main.legend_ext)
        heatmap_legend.build_ui()
        heatmap_legend.show_legend()

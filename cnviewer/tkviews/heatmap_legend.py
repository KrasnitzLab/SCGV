'''
Created on Feb 8, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport

from tkviews.legend_base import LegendBase
from utils.color_map import ColorMap


class HeatmapLegend(LegendBase):
    COPYNUM_LABELS = [
        "    0", "    1", "    2", "    3", "    4+"
    ]

    def __init__(self, master, controller):
        super(HeatmapLegend, self).__init__(
            master,
            title="Heatmap Legend",
            controller=controller)

    def show_legend(self):
        cmap = ColorMap.make_diverging05()
        for index, label in enumerate(self.COPYNUM_LABELS):
            color = cmap.colors(index)
            self.append_entry(label, color)

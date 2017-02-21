'''
Created on Feb 8, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport

from tkutils.legend_base import LegendBase
# import matplotlib.pyplot as plt
from views.base import ViewerBase
from utils.color_map import ColorMap


class HeatmapLegend(LegendBase):

    def __init__(self, master):
        super(HeatmapLegend, self).__init__(
            master, title="Heatmap Legend")

    def show_legend(self):
        cmap = ColorMap.make_diverging05()
        for index, label in enumerate(ViewerBase.COPYNUM_LABELS):
            color = cmap.colors(index)
            self.append_entry(label, color)

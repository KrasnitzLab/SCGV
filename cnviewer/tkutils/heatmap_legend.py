'''
Created on Feb 8, 2017

@author: lubo
'''
import sys  # @UnusedImport
from tkutils.legend_base import LegendBase
# import matplotlib.pyplot as plt
from views.base import ViewerBase
from utils.color_map import ColorMap

if sys.version_info[0] < 3:
    import Tkinter as tk  # @UnusedImport @UnresolvedImport
    import ttk  # @UnusedImport @UnresolvedImport
    from tkFileDialog import askopenfilename  # @UnusedImport @UnresolvedImport
    import tkMessageBox as messagebox  # @UnusedImport @UnresolvedImport
else:
    import tkinter as tk  # @Reimport @UnresolvedImport @UnusedImport
    from tkinter import ttk  # @UnresolvedImport @UnusedImport @Reimport
    from tkinter.filedialog \
        import askopenfilename  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter.filedialog \
        import askdirectory  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter import messagebox  # @UnresolvedImport @Reimport @UnusedImport


class HeatmapLegend(LegendBase):

    def __init__(self, master):
        super(HeatmapLegend, self).__init__(
            master, title="Heatmap Legend")

    def show_legend(self):
        cmap = ColorMap.make_diverging05()
        for index, label in enumerate(ViewerBase.COPYNUM_LABELS):
            color = cmap.colors(index)
            self.append_entry(label, color)

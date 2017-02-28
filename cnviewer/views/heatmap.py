'''
Created on Dec 14, 2016

@author: lubo
'''
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches

# from utils.color_map import ColorMap
from views.base import ViewerBase
from utils.color_map import ColorMap


class HeatmapViewer(ViewerBase):

    def __init__(self, model):
        super(HeatmapViewer, self).__init__(model)
        self.cmap = ColorMap.make_diverging05()

    def draw_heatmap(self, ax):
        if self.model.heatmap is None:
            return

        ax.imshow(self.model.heatmap,
                  aspect='auto',
                  interpolation='nearest',
                  # cmap=plt.get_cmap('seismic'),  # self.cmap.colors,
                  cmap=self.cmap.colors,
                  vmin=self.NORMALIZE_MIN,
                  vmax=self.NORMALIZE_MAX,
                  # norm=self.cmap.norm,
                  extent=self.model.heat_extent)

        chrom_lines = self.model.calc_chrom_lines_index()
        for chrom_line in chrom_lines:
            ax.axhline(y=chrom_line, color="#888888", linewidth=0.5)
        chrom_labelspos = self.calc_chrom_labels_pos(chrom_lines)
        ax.set_yticks(chrom_labelspos)
        ax.set_yticklabels(self.CHROM_LABELS, fontsize=9)

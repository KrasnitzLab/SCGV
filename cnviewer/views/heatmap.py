'''
Created on Dec 14, 2016

@author: lubo
'''
import matplotlib.pyplot as plt
# import matplotlib.patches as patches

# from utils.color_map import ColorMap
from views.base import ViewerBase
from utils.color_map import ColorMap


class HeatmapViewer(ViewerBase):

    def __init__(self, model):
        super(HeatmapViewer, self).__init__(model)
        self.cmap = ColorMap.make_deverging09()

    def draw_heatmap(self, ax):
        assert self.model.heatmap is not None

        ax.imshow(self.model.heatmap,
                  aspect='auto',
                  interpolation='nearest',
                  cmap=plt.get_cmap('seismic'),  # self.cmap.colors,
                  # cmap=self.cmap.colors,
                  vmin=self.NORMALIZE_MIN,
                  vmax=self.NORMALIZE_MAX,
                  # norm=self.cmap.norm,
                  extent=self.model.heat_extent)
        ax.set_xticks(self.model.label_midpoints)
        ax.set_xticklabels(self.model.column_labels,
                           rotation='vertical',
                           fontsize=10)
        chrom_lines = self.calc_chrom_lines_pos(self.model.seg_df)
        for chrom_line in chrom_lines:
            plt.axhline(y=chrom_line, color="#000000", linewidth=1)
        chrom_labelspos = self.calc_chrom_labels_pos(chrom_lines)
        ax.set_yticks(chrom_labelspos)
        ax.set_yticklabels(self.CHROM_LABELS, fontsize=9)

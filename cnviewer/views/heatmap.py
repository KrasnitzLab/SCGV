'''
Created on Dec 14, 2016

@author: lubo
'''
import matplotlib.pyplot as plt
# import matplotlib.patches as patches

from utils.color_map import ColorMap
from views.base import ViewerBase


class HeatmapViewer(ViewerBase):

    def __init__(self, model):
        super(HeatmapViewer, self).__init__(model)
        self.cmap = ColorMap.make_cmap02()
        # self.cmap = ColorMap.make_cmap08()

    #     def draw_legend(self):
    #         copynum_patches = []
    #         for color in self.cmap.colors.colors:
    #             copynum_patches.append(
    #                 patches.Rectangle((0, 0), 0, 0, facecolor=color))
    #         plt.figlegend(
    #             copynum_patches, self.COPYNUM_LABELS, "upper right",
    #             title="Copy #", prop={'size': 10})

    def draw_heatmap(self, ax):
        assert self.model.heatmap is not None

        # ax.imshow(self.model.heatmap,
        ax.imshow(self.model.seg_data,
                  aspect='auto',
                  interpolation='nearest',
                  cmap=plt.get_cmap('seismic'),  # self.cmap.colors,
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

#     def draw(self, fig=None):
#         if fig is None:
#             fig = plt.gcf()
#
#         ax_dendro = fig.add_axes([0.1, 0.75, 0.8, 0.2], frame_on=True)
#         self.draw_dendrogram(ax_dendro)
#         self.clear_xlabels(ax_dendro)
#
#         ax_heat = fig.add_axes(
#             [0.1, 0.10, 0.8, 0.65], frame_on=True, sharex=ax_dendro)
#         self.draw_heatmap(ax_heat)
#         self.make_legend()

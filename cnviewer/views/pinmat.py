'''
Created on Jan 4, 2017

@author: lubo
'''
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches

# from utils.color_map import ColorMap
from views.base import ViewerBase
from utils.color_map import ColorMap


class PinmatViewer(ViewerBase):

    NORMALIZE_PINS_MIN = -2
    NORMALIZE_PINS_MAX = 2

    def __init__(self, model):
        super(PinmatViewer, self).__init__(model)
        self.cmap = ColorMap.make_diverging05()

    def draw_heatmap(self, ax):
        if self.model.pinmat is None:
            return

        ax.imshow(self.model.pins,
                  aspect='auto',
                  interpolation='nearest',
                  # cmap=plt.get_cmap('seismic'),
                  cmap=self.cmap.colors,
                  vmin=self.NORMALIZE_PINS_MIN,
                  vmax=self.NORMALIZE_PINS_MAX,
                  extent=self.model.heat_extent)
        ax.set_xticks(self.model.label_midpoints)
        ax.set_xticklabels(self.model.column_labels,
                           rotation='vertical',
                           fontsize=10)

        chrom_lines = self.model.calc_chrom_lines_index()
        for chrom_line in chrom_lines:
            ax.axhline(y=chrom_line, color="#888888", linewidth=0.5)
        chrom_labelspos = self.calc_chrom_labels_pos(chrom_lines)
        ax.set_yticks(chrom_labelspos)
        ax.set_yticklabels(self.CHROM_LABELS, fontsize=9)

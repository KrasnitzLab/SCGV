'''
Created on Dec 2, 2016

@author: lubo
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from utils.loader import load_df
from scipy.cluster.hierarchy import linkage, dendrogram
from utils.color_map import ColorMap


class Viewer(object):
    CHROM_LABELS = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
        "14", "15", "16", "17", "18", "19", "20", "21", "22", "X", "Y"
    ]

    COPYNUM_LABELS = ["0", "1", "2", "3", "4", "5+"]

    def __init__(self, df):
        self.df = df
        self.data = df.ix[:, 3:].values
        self.bins, self.samples = self.data.shape
        self.interval_length = None
        self.Z = None
        self.lmat = None
        self.cmap = ColorMap.make_cmap01()

    def make_chrom_lines(self):
        assert self.df is not None
        chrom_pos = self.df.chrom.values
        chrom_shift = np.roll(chrom_pos, -1)
        chrom_boundaries = chrom_pos != chrom_shift
        chrom_boundaries[0] = True
        chrom_lines = np.where(chrom_boundaries)
        return chrom_lines[0]

    def make_chrom_labelspos(self, chrom_lines):
        yt = (np.roll(chrom_lines, -1) - chrom_lines) / 2.0
        return (chrom_lines + yt)[:-1]

    def draw_dendogram(self, ax):
        assert self.data is not None
        if self.lmat is None:
            self.lmat = linkage(self.data.transpose(), method='ward')
        if self.Z is None:
            self.Z = dendrogram(self.lmat, ax=ax)
            min_x = np.min(self.Z['icoord'])
            max_x = np.max(self.Z['icoord'])
            self.interval_length = \
                (max_x - min_x) / (self.samples - 1)
            self.direct_lookup = self.Z['leaves']
            self.column_labels = \
                np.array(self.df.columns[3:])[self.direct_lookup]
            self.label_midpoints = \
                (np.arange(self.samples) + 0.5) * self.interval_length

        ax.set_xticks(self.label_midpoints)
        ax.set_xticklabels([''] * len(self.column_labels))

    def make_legend(self):
        copynumPatches = []
        for a in self.cmap.colors.colors:
            copynumPatches.append(patches.Rectangle((0, 0), 0, 0, facecolor=a))

        plt.figlegend(copynumPatches, self.COPYNUM_LABELS, "upper right",
                      title="Copy #", prop={'size': 10})

    def draw_heatmap(self, ax):
        heat_extent = (0, self.samples * self.interval_length,
                       self.bins, 0)
        data = np.round(self.data)

        ax.imshow(data[:, self.direct_lookup],
                  aspect='auto',
                  interpolation='nearest',
                  cmap=self.cmap.colors,
                  norm=self.cmap.norm,
                  extent=heat_extent)
        ax.set_xticks(self.label_midpoints)
        ax.set_xticklabels(self.column_labels,
                           rotation='vertical',
                           fontsize=10)
        chrom_lines = self.make_chrom_lines()
        for chrom_line in chrom_lines:
            plt.axhline(y=chrom_line, color="#000000", linewidth=1)
        chrom_labelspos = self.make_chrom_labelspos(chrom_lines)
        ax.set_yticks(chrom_labelspos)
        ax.set_yticklabels(self.CHROM_LABELS, fontsize=9)


def main():
    seg_filename = 'tests/data/sample.YL2671P11.5k.seg.quantal.primary.txt'
    df = load_df(seg_filename)

    assert df is not None

    viewer = Viewer(df)

    fig = plt.figure(0, figsize=(12, 8))
    fig.suptitle(seg_filename, fontsize=10)

    ax_dendro = fig.add_axes([0.1, 0.75, 0.8, 0.2], frame_on=True)
    # draw_dendrogram(df, ax_dendro)
    viewer.draw_dendogram(ax_dendro)

    ax_heat = fig.add_axes(
        [0.1, 0.10, 0.8, 0.65], frame_on=True, sharex=ax_dendro)
    viewer.draw_heatmap(ax_heat)
    viewer.make_legend()

    plt.show()

if __name__ == '__main__':
    main()

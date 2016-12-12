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

    def make_column_labels(self):
        assert self.direct_lookup
        assert self.df is not None

        self.column_labels = \
            np.array(self.df.columns[3:])[self.direct_lookup]
        return self.column_labels

    def make_dendrogram(self, ax, no_plot=False):
        if self.Z is not None:
            return
        self.Z = dendrogram(self.lmat, ax=ax, no_plot=no_plot)
        min_x = np.min(self.Z['icoord'])
        max_x = np.max(self.Z['icoord'])
        self.interval_length = (max_x - min_x) / (self.samples - 1)
        self.direct_lookup = self.Z['leaves']
        self.label_midpoints = (
            np.arange(self.samples) + 0.5) * self.interval_length
        self.make_column_labels()

    def make_linkage(self):
        if self.lmat is not None:
            return
        self.lmat = linkage(self.data.transpose(), method='ward')

    def draw_dendogram(self, ax):
        assert self.data is not None
        self.make_linkage()
        self.make_dendrogram(ax)

        ax.set_xticks(self.label_midpoints)
        ax.set_xticklabels([''] * len(self.column_labels))

    def make_legend(self):
        copynum_patches = []
        for color in self.cmap.colors.colors:
            copynum_patches.append(
                patches.Rectangle((0, 0), 0, 0, facecolor=color))
        plt.figlegend(copynum_patches, self.COPYNUM_LABELS, "upper right",
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

    @staticmethod
    def debug_event(event):
        # print(event)
        if event.name == 'button_press_event':
            print("MOUSE: name={}; xy=({},{}); xydata=({},{}); "
                  "button={}; dblclick={}".format(
                      event.name,
                      event.x, event.y,
                      event.xdata, event.ydata,
                      event.button, event.dblclick
                  ))
        elif event.name == 'key_press_event':
            print("KEY: name={}; xy=({},{}); xydata=({},{}); "
                  "key={}".format(
                      event.name,
                      event.x, event.y,
                      event.xdata, event.ydata,
                      event.key
                  ))
        else:
            print("???: {}".format(event.name))

    def locate_sample_click(self, event):
        if event.xdata is None:
            return None
        xloc = int(event.xdata / self.interval_length)
        sample_name = self.column_labels[xloc]
        print("xloc: {}; sample name: {}".format(xloc, sample_name))
        return sample_name

    def event_handler(self, event):
        print("event tester called...")
        Viewer.debug_event(event)
        self.locate_sample_click(event)

    def event_loop_connect(self, fig):
        fig.canvas.mpl_connect('button_press_event', self.event_handler)
        fig.canvas.mpl_connect('key_press_event', self.event_handler)


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

    viewer.event_loop_connect(fig)

    plt.show()

if __name__ == '__main__':
    main()

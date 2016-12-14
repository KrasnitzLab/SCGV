'''
Created on Dec 14, 2016

@author: lubo
'''
from scipy.cluster.hierarchy import linkage, dendrogram

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np
from utils.color_map import ColorMap
from views.base import ViewerBase


class HeatmapViewer(ViewerBase):

    def __init__(self, seg_df):
        super(HeatmapViewer, self).__init__()
        self.seg_df = seg_df
        self.seg_data = seg_df.ix[:, 3:].values
        self.bins, self.samples = self.seg_data.shape
        self.interval_length = None
        self.Z = None
        self.lmat = None
        self.cmap = ColorMap.make_cmap01()
        self.sample_list = []

    def make_column_labels(self):
        assert self.direct_lookup
        assert self.seg_df is not None

        self.column_labels = \
            np.array(self.seg_df.columns[3:])[self.direct_lookup]
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
        self.lmat = linkage(self.seg_data.transpose(), method='ward')

    def draw_dendogram(self, ax):
        assert self.seg_data is not None
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
        data = np.round(self.seg_data)

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
        chrom_lines = self.calc_chrom_lines_pos(self.seg_df)
        for chrom_line in chrom_lines:
            plt.axhline(y=chrom_line, color="#000000", linewidth=1)
        chrom_labelspos = self.calc_chrom_label_spos(chrom_lines)
        ax.set_yticks(chrom_labelspos)
        ax.set_yticklabels(self.CHROM_LABELS, fontsize=9)

    def locate_sample_click(self, event):
        if event.xdata is None:
            return None
        xloc = int(event.xdata / self.interval_length)
        sample_name = self.column_labels[xloc]
        print("xloc: {}; sample name: {}".format(xloc, sample_name))
        return sample_name

    def event_handler(self, event):
        print("event tester called...")
        self.debug_event(event)
        if event.name == 'button_press_event':
            sample = self.locate_sample_click(event)
            self.add_sample(sample)
        elif event.name == 'key_press_event' and event.key == 'd':
            print(self.sample_list)

            self.display_samples()
            self.sample_list = []

    def event_loop_connect(self, fig):
        fig.canvas.mpl_connect('button_press_event', self.event_handler)
        fig.canvas.mpl_connect('key_press_event', self.event_handler)

    def add_sample(self, sample):
        if sample is None:
            return
        if sample in self.sample_list:
            return
        self.sample_list.append(sample)

    def display_samples(self):
        pass

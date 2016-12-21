'''
Created on Dec 14, 2016

@author: lubo
'''
from views.base import ViewerBase
from scipy.cluster.hierarchy import linkage, dendrogram

import numpy as np


class DendrogramViewer(ViewerBase):

    def __init__(self, seg_df, tree_df=None):
        super(DendrogramViewer, self).__init__(seg_df)

        self.lmat = self.make_linkage(tree_df)
        self.Z = None
        self.direct_lookup = None
        self.column_labels = None

    def make_linkage(self, tree_df):
        if tree_df is None:
            return linkage(self.seg_data.transpose(), method='ward')
        else:
            assert len(tree_df) + 1 == self.samples

            tree_df.height = -1 * tree_df.height
            max_height = tree_df.height.max()
            tree_df.height = 1.11 * max_height - tree_df.height
            return tree_df.values

    def make_column_labels(self):
        assert self.direct_lookup
        assert self.seg_df is not None

        self.column_labels = \
            np.array(self.seg_df.columns[3:])[self.direct_lookup]
        return self.column_labels

    def _draw_dendrogram(self, ax):
        assert self.Z is not None

        dcoord = np.array(self.Z['dcoord'])
        max_dcoord = np.max(dcoord)
        dcoord_hang = 0.1 * max_dcoord

        ys = dcoord[:, 1] - dcoord_hang
        ys[ys < 0] = 0
        zeros = dcoord[:, 0] == 0
        dcoord[zeros, 0] = ys[zeros]

        ys = dcoord[:, 2] - dcoord_hang
        ys[ys < 0] = 0
        zeros = dcoord[:, 3] == 0
        dcoord[zeros, 3] = ys[zeros]

        icoord = np.array(self.Z['icoord'])
        color_list = np.array(self.Z['color_list'])

        min_x = np.min(icoord)
        max_x = np.max(icoord)

        min_y = np.min(dcoord)
        max_y = np.max(dcoord)

        for xs, ys, color in zip(icoord, dcoord, color_list):
            ax.plot(xs, ys, color)
        ax.set_xlim(min_x - 10, max_x + 10)
        ax.set_ylim(min_y, max_y + 0.05 * max_y)

    def make_dendrogram(self):
        if self.Z is not None:
            return
        self.Z = dendrogram(self.lmat, ax=None, no_plot=True)

        min_x = np.min(self.Z['icoord'])
        max_x = np.max(self.Z['icoord'])
        self.interval_length = (max_x - min_x) / (self.samples - 1)
        self.direct_lookup = self.Z['leaves']

        self.label_midpoints = (
            np.arange(self.samples) + 0.5) * self.interval_length
        self.make_column_labels()

    def draw_dendrogram(self, ax):
        self.make_dendrogram()
        self._draw_dendrogram(ax)
        self.clear_labels(ax)

    def clear_labels(self, ax):
        ax.set_xticks(self.label_midpoints)
        ax.set_xticklabels([''] * len(self.column_labels))

    def draw_labels(self, ax):
        ax.set_xticks(self.label_midpoints)
        ax.set_xticklabels(self.column_labels,
                           rotation='vertical',
                           fontsize=10)

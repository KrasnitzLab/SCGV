'''
Created on Dec 14, 2016

@author: lubo
'''
from views.base import ViewerBase
from scipy.cluster.hierarchy import linkage, dendrogram

import numpy as np


class DendrogramViewer(ViewerBase):

    def __init__(self, seg_df, tree_df=None):
        super(DendrogramViewer, self).__init__()

        self.seg_df = seg_df
        self.seg_data = self.seg_df.ix[:, 3:].values
        self.bins, self.samples = self.seg_data.shape

        self.lmat = self.make_linkage(tree_df)
        self.Z = None

    def make_linkage(self, tree_df):
        if tree_df is None:
            return linkage(self.seg_data.transpose(), method='ward')
        else:
            max_height = tree_df.height.max()
            tree_df.height = 1.11 * max_height - tree_df.height
            return tree_df.values

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

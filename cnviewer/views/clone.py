'''
Created on Dec 15, 2016

@author: lubo
'''
import numpy as np
from views.base import BarViewerBase


class CloneViewer(BarViewerBase):
    CLONE_COLUMN = 'clone'
    SUBCLONE_COLUMN = 'subclone'

    def __init__(self, dendrogram, clone_df):
        super(CloneViewer, self).__init__(dendrogram)
        self.clone_df = clone_df
        self.clone = None
        self.subclone = None

    def make_clone(self):
        assert self.dendrogram.direct_lookup is not None
        labels = self.clone_df.ix[self.dendrogram.direct_lookup, 0].values
        assert np.all(labels == self.dendrogram.column_labels)

        clone_column_df = self.clone_df.iloc[self.dendrogram.direct_lookup, :]
        self.clone = self._build_heatmap_array(
            clone_column_df[self.CLONE_COLUMN])
        self.subclone = self._build_heatmap_array(
            clone_column_df[self.SUBCLONE_COLUMN])

    def draw_clone(self, ax):
        assert self.clone is not None
        assert self.subclone is not None

        ax.imshow(
            self.clone, aspect='auto', interpolation='nearest',
            cmap=self.cmap.colors, norm=self.cmap.norm, extent=self.extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.0])
        ax.set_yticklabels(["Clone"])

    def draw_subclone(self, ax):
        assert self.clone is not None
        assert self.subclone is not None

        ax.imshow(
            self.subclone, aspect='auto', interpolation='nearest',
            cmap=self.cmap.colors, norm=self.cmap.norm, extent=self.extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_yticklabels([])

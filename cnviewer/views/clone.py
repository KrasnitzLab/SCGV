'''
Created on Dec 15, 2016

@author: lubo
'''
import numpy as np
import pandas as pd

from utils.color_map import ColorMap


class CloneViewer(object):

    def __init__(self, dendrogram, clone_df):
        self.dendrogram = dendrogram
        self.clone_df = clone_df
        self.clone = None
        self.subclone = None
        self._extent = None
        self._cmap = None
        self._color_counter = 1

    def make_clone(self):
        assert self.dendrogram.direct_lookup is not None
        labels = self.clone_df.ix[self.dendrogram.direct_lookup, 0].values
        assert np.all(labels == self.dendrogram.column_labels)

        clone_column_df = self.clone_df.iloc[self.dendrogram.direct_lookup, :]
        self.clone = self._build_heatmap_array(clone_column_df['clone'])
        self.subclone = self._build_heatmap_array(clone_column_df['subclone'])

    def _build_heatmap_array(self, df):
        unique = df.unique()
        result = pd.Series(index=df.index)
        for val in unique:
            if val == 0:
                result[df == val] = 0
            else:
                result[df == val] = self._color_counter
                self._color_counter += 1

        return np.array([result.values])

    @property
    def extent(self):
        if self._extent is None:
            self._extent = (
                0, self.dendrogram.samples * self.dendrogram.interval_length,
                0, 1)
        return self._extent

    @property
    def cmap(self):
        if self._cmap is None:
            self._cmap = ColorMap.make_cmap07()
        return self._cmap

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

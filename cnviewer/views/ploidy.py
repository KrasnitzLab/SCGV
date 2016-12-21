'''
Created on Dec 21, 2016

@author: lubo
'''
import numpy as np
from views.base import BarViewerBase


class PloidyViewer(BarViewerBase):
    PLOIDY_COLUMN = 'ploidy'
    SAMPLES_COLUMN = 'seq.unit.id'

    def __init__(self, dendrogram, guide_df):
        super(PloidyViewer, self).__init__(dendrogram)
        assert self.PLOIDY_COLUMN in guide_df.columns
        self.guide_df = guide_df
        self.ploidy = None

    def make_ploidy(self):
        assert self.dendrogram.direct_lookup is not None
        labels = self.guide_df[self.SAMPLES_COLUMN].ix[
            self.dendrogram.direct_lookup].values
        assert np.all(labels == self.dendrogram.column_labels)

        ploidy_column_df = self.guide_df.iloc[self.dendrogram.direct_lookup, :]
        self.ploidy = self._build_heatmap_array(
            ploidy_column_df[self.PLOIDY_COLUMN])

    def draw_ploidy(self, ax):
        assert self.ploidy is not None
        ax.imshow(
            self.ploidy, aspect='auto', interpolation='nearest',
            cmap=self.cmap.colors, norm=self.cmap.norm, extent=self.extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Ploidy"])

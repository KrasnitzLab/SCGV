'''
Created on Dec 21, 2016

@author: lubo
'''
import numpy as np
from matplotlib import cm
from views.base import BarViewerBase


class MultiplierViewer(BarViewerBase):

    def __init__(self, dendrogram, seg_df):
        super(MultiplierViewer, self).__init__(dendrogram)
        self.seg_df = seg_df
        self._chrom_x_index = None

    @property
    def chrom_x_index(self):
        if self._chrom_x_index is None:
            self._chrom_x_index = np.where(self.seg_df['chrom'] == 23)[0][0]
        return self._chrom_x_index

    def make_multiplier(self):
        data = self.seg_df.iloc[:self.chrom_x_index, 3:]
        self.multiplier = data.mean(axis=1).ix[
            self.dendrogram.direct_lookup].values

    def draw_multiplier(self, ax):
        ax.imshow(
            [self.multiplier],
            aspect='auto',
            interpolation='nearest',
            cmap=cm.coolwarm,  # @UndefinedVariable
            extent=self.extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Multiplier"])

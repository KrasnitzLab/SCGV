'''
Created on Dec 21, 2016

@author: lubo
'''
from matplotlib import cm

import numpy as np
from views.multiplier import MultiplierViewer


class ErrorViewer(MultiplierViewer):

    def __init__(self, dendrogram, seg_df, ratio_df):
        super(ErrorViewer, self).__init__(dendrogram, seg_df)
        self.ratio_df = ratio_df

    def make_error(self):
        df_s = self.seg_df.iloc[:self.chrom_x_index, 3:].values
        df_r = self.ratio_df.iloc[:self.chrom_x_index, 3:].values
        self.error = np.sqrt(np.sum(((df_r - df_s) / df_s)**2, axis=1))[
            self.dendrogram.direct_lookup]

    def draw_error(self, ax):
        ax.imshow(
            [self.error],
            aspect='auto',
            interpolation='nearest',
            cmap=cm.coolwarm,  # @UndefinedVariable
            extent=self.extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Error"])

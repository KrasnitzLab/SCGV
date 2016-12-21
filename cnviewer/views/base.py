'''
Created on Dec 14, 2016

@author: lubo
'''
import numpy as np
import pandas as pd
from utils.color_map import ColorMap


class ViewerBase(object):
    CHROM_LABELS = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
        "14", "15", "16", "17", "18", "19", "20", "21", "22", "X", "Y"
    ]

    COPYNUM_LABELS = [
        "0", "med - 2+", "med - 1", "median", "med + 1", "med + 2+"
    ]

    PLOIDY_LABELS = ["<2C", "2C", ">2C-4C", "4C", ">4C"]

    def __init__(self, seg_df):
        self.seg_df = seg_df
        self.seg_data = self.seg_df.ix[:, 3:].values
        self.bins, self.samples = self.seg_data.shape

    @staticmethod
    def calc_chrom_lines_pos(df):
        assert df is not None
        chrom_pos = df.chrom.values
        chrom_shift = np.roll(chrom_pos, -1)
        chrom_boundaries = chrom_pos != chrom_shift
        chrom_boundaries[0] = True
        chrom_lines = np.where(chrom_boundaries)
        return chrom_lines[0]

    @staticmethod
    def calc_chrom_labels_pos(chrom_lines):
        yt = (np.roll(chrom_lines, -1) - chrom_lines) / 2.0
        return (chrom_lines + yt)[:-1]


class BarViewerBase(object):

    def __init__(self, dendrogram):
        self.dendrogram = dendrogram
        self._extent = None
        self._cmap = None
        self._color_counter = 1

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

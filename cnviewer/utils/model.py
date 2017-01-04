'''
Created on Dec 21, 2016

@author: lubo
'''
from scipy.cluster.hierarchy import dendrogram

import numpy as np
import pandas as pd

from utils.loader import DataLoader


class DataModel(DataLoader):
    CLONE_COLUMN = 'clone'
    SUBCLONE_COLUMN = 'subclone'
    GATE_COLUMN = 'gate'
    CHROM_COLUMN = 'chrom'

    def __init__(self, zip_filename):
        super(DataModel, self).__init__(zip_filename)
        self.seg_data = self.seg_df.ix[:, 3:].values
        self.bins, self.samples = self.seg_data.shape
        self.lmat = None
        self.Z = None

        self._chrom_x_index = None
        self._bar_extent = None

    @property
    def heat_extent(self):
        return (0, self.samples * self.interval_length,
                self.bins, 0)

    @property
    def chrom_x_index(self):
        if self._chrom_x_index is None:
            self._chrom_x_index = \
                np.where(self.seg_df[self.CHROM_COLUMN] == 23)[0][0]
        return self._chrom_x_index

    def make(self):
        self.make_linkage()
        self.make_dendrogram()
        self.make_pinmat()
        self.make_heatmap()
        self.make_clone()
        self.make_gate()
        self.make_multiplier()
        self.make_error()

    def make_linkage(self):
        if self.lmat is not None:
            return
        assert len(self.tree_df) + 1 == self.samples
        df = self.tree_df.copy()

        df.height = -1 * df.height
        max_height = df.height.max()
        df.height = 1.11 * max_height - df.height
        self.lmat = df.values

    def make_dendrogram(self):
        if self.Z is not None:
            return
        self.Z = dendrogram(
            self.lmat, ax=None, no_plot=True, color_threshold=99999999)
        self.icoord = np.array(self.Z['icoord'])
        self.dcoord = np.array(self.Z['dcoord'])
        self.min_x = np.min(self.icoord)
        self.max_x = np.max(self.icoord)
        self.interval_length = (self.max_x - self.min_x) / (self.samples - 1)
        self.direct_lookup = self.Z['leaves']
        self.column_labels = \
            np.array(self.seg_df.columns[3:])[self.direct_lookup]
        self.label_midpoints = (
            np.arange(self.samples) + 0.5) * self.interval_length

    @staticmethod
    def _make_heatmap_array(df):
        color_counter = 1
        unique = df.unique()
        result = pd.Series(index=df.index)
        for val in unique:
            if val == 0:
                result[df == val] = 0
            else:
                result[df == val] = color_counter
                color_counter += 1

        return result.values

    def make_heatmap(self):
        data = np.round(self.seg_data)
        self.heatmap = data[:, self.direct_lookup]

    def make_pinmat(self):
        assert self.bins is not None
        assert self.samples is not None
        assert self.pins_df is not None
        assert self.pinmat_df is not None

        self.pinmat_df = self.pinmat_df.ix[:, self.direct_lookup].copy()
        assert np.all(list(self.pinmat_df.columns) == self.column_labels)

        pins = np.zeros((self.bins, self.samples))
        negative = self.pins_df[self.pins_df.sign == -1].bin
        positive = self.pins_df[self.pins_df.sign == 1].bin

        # assert len(negative) + len(positive) == self.bins
        pins[negative, :] = -1 * self.pinmat_df.ix[negative.index, :].values
        pins[positive, :] = 1 * self.pinmat_df.ix[positive.index, :].values

        psi = int(self.bins / 600)
        kernel = np.ones(2 * psi)
        self.pins = np.apply_along_axis(
            np.convolve,
            0,
            pins,
            kernel,
            'same')
        # self.pins = pins
        # self.pins = self.pins - self.expected
        # self.pins = pins

    def make_clone(self):
        assert self.direct_lookup is not None
        labels = self.clone_df.ix[self.direct_lookup, 0].values
        assert np.all(labels == self.column_labels)

        clone_column_df = self.clone_df.iloc[self.direct_lookup, :]
        self.clone = self._make_heatmap_array(
            clone_column_df[self.CLONE_COLUMN])
        self.subclone = self._make_heatmap_array(
            clone_column_df[self.SUBCLONE_COLUMN])

    GATE_MAPPING = {
        'Diploid': 2,
        'Hypodiploid': 1.8,
        'Haploid': 1,
        '4C': 4,
        '2C': 2,
        '2C Rt': 2.01,
        'Aneuploid': 1.99,
        '2C EpCAM Neg': 1.95,
        '>2C': 2.25,
        '<2C EpCAM Pos': 1.5,
        '>2C-4C EpCAM Pos': 2.5,
        '4C EpCAM Pos': 4,
        '2C Rt EpCAM Pos': 2,
        '2C Lt EpCAM Pos': 2,
        '>4C EpCAM Pos': 4,
        '2C EpCAM Pos': 2,
        '>2C EpCAM Pos': 2.5,
        '2C Lt': 2,
        '<2C': 1.5,
        '>2C-4C': 3, '>2C-4C Lt': 3,
        '>2C-4C Rt': 3,
        '>4C': 4,
        'Near 2C': 2,
        'Bulk Nuclei': np.nan,
        'Single Nuclei': np.nan,
        '10000 nuclei': np.nan,
        '100 nuclei': np.nan,
        'A1': np.nan,
        'A2': np.nan,
        'Aneuploid': np.nan,
        'Bulk Tissue': np.nan,
        'Blood': np.nan,
        'Micronuc': np.nan
    }

    def make_gate(self):
        if self.GATE_COLUMN not in self.guide_df.columns:
            self.gate = None
            return

        assert self.direct_lookup is not None
        labels = self.guide_df[self.GUIDE_SAMPLES_COLUMN].ix[
            self.direct_lookup].values
        assert np.all(labels == self.column_labels)

        gate_column_df = self.guide_df.iloc[self.direct_lookup, :]
#         gate = sorted(
#             gate_column_df[self.GATE_COLUMN].unique(), cmp=gate_compare)
        self.gate = np.array(map(
            lambda g: self.GATE_MAPPING.get(g, 2),
            gate_column_df[self.GATE_COLUMN].values
        ))

    def make_multiplier(self):
        data = self.seg_df.iloc[:self.chrom_x_index, 3:]
        multiplier = data.mean(axis=1).ix[self.direct_lookup]
        self.multiplier = multiplier.values

    def make_error(self):
        df_s = self.seg_df.iloc[:self.chrom_x_index, 3:].values
        df_r = self.ratio_df.iloc[:self.chrom_x_index, 3:].values
        self.error = np.sqrt(np.sum(((df_r - df_s) / df_s)**2, axis=1))[
            self.direct_lookup]
        print(np.unique(self.error))

    @property
    def bar_extent(self):
        if self._bar_extent is None:
            self._bar_extent = (
                0, self.samples * self.interval_length,
                0, 1)
        return self._bar_extent


def gate_compare(g1, g2):
    assert len(g1) >= 2
    assert len(g2) >= 2

    if g1[0] == '>' or g1[0] == '<':
        sg1 = g1[1:].strip()
        sign1 = sg1[0]
    else:
        sg1 = g1
        sign1 = None

    if g2[0] == '>' or g2[0] == '<':
        sg2 = g2[1:].strip()
        sign2 = g2[0]
    else:
        sg2 = g2
        sign2 = None
    assert len(sg1) >= 2
    assert len(sg2) >= 2

    if sg1[:2] == sg2[:2] and (sign1 or sign2):
        if sign1 and sign2:
            if sign1 > sign2:
                return 1
            elif sign1 < sign2:
                return -1
            else:
                return 0
        else:
            if sign1:
                if sign1 == '<':
                    return -1
                elif sign1 == '>':
                    return 1
                assert False
            elif sign2:
                if sign2 == '<':
                    return 1
                elif sign2 == '>':
                    return -1
                assert False
    if sg1 > sg2:
        return 1
    elif sg1 < sg2:
        return -1
    else:
        return 0

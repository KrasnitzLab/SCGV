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
    SECTOR_COLUMN = 'sector'
    PATHOLOGY_COLUMN = 'Pathology'

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
        ordering = self.make_dendrogram()

        self.clone, self.subclone = self.make_clone(ordering=ordering)

        self.pins = self.make_pinmat(ordering=ordering)
        self.heatmap = self.make_heatmap(ordering=ordering)
        self.gate = self.make_gate(ordering=ordering)
        self.sector = self.make_sector(ordering=ordering)
        self.multiplier = self.make_multiplier(ordering=ordering)
        self.error = self.make_error(ordering=ordering)

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
        ordering = np.array(self.Z['leaves'])

        self.column_labels = \
            np.array(self.seg_df.columns[3:])[ordering]
        self.label_midpoints = (
            np.arange(self.samples) + 0.5) * self.interval_length
        return ordering

    @classmethod
    def _reset_heatmap_color(cls):
        cls.heatmap_color_counter = 1

    @classmethod
    def _make_heatmap_array(cls, df):
        unique = df.unique()
        unique.sort()
        print(unique)
        result = pd.Series(index=df.index)
        for val in unique:
            if val == 0:
                result[df == val] = 0
            else:
                result[df == val] = cls.heatmap_color_counter
                cls.heatmap_color_counter += 1

        return result.values

    def make_heatmap(self, ordering):
        data = np.round(self.seg_data)
        return data[:, ordering]

    def make_pinmat(self, ordering):
        assert self.bins is not None
        assert self.samples is not None
        assert self.pins_df is not None
        assert self.pinmat_df is not None

        self.pinmat_df = self.pinmat_df.ix[:, ordering].copy()
        assert np.all(list(self.pinmat_df.columns) == self.column_labels)

        pins = np.zeros((self.bins, self.samples))
        negative = self.pins_df[self.pins_df.sign == -1].bin
        positive = self.pins_df[self.pins_df.sign == 1].bin

        # assert len(negative) + len(positive) == self.bins
        pins[negative, :] = -1 * self.pinmat_df.ix[negative.index, :].values
        pins[positive, :] = 1 * self.pinmat_df.ix[positive.index, :].values

        psi = int(self.bins / 600)
        kernel = np.ones(2 * psi)
        return np.apply_along_axis(
            np.convolve,
            0,
            pins,
            kernel,
            'same')
        # self.pins = pins
        # self.pins = self.pins - self.expected
        # self.pins = pins

    def make_clone(self, ordering):
        assert ordering is not None

        clone_column_df = self.clone_df.iloc[ordering, :]
        self._reset_heatmap_color()
        clone = self._make_heatmap_array(
            clone_column_df[self.CLONE_COLUMN])
        subclone = self._make_heatmap_array(
            clone_column_df[self.SUBCLONE_COLUMN])
        return clone, subclone

    EPCAM = {
        '2C EpCAM Neg': 2,
        '<2C EpCAM Pos': 1.5,
        '>2C-4C EpCAM Pos': 3,
        '4C EpCAM Pos': 4,
        '2C Rt EpCAM Pos': 2.25,
        '2C Lt EpCAM Pos': 1.75,
        '>4C EpCAM Pos': 5,
        '2C EpCAM Pos': 2,
        '>2C EpCAM Pos': 2.5,
    }
    GATE_MAPPING = {
        '4C': 4,
        '2C': 2,
        '2C Rt': 2.25,
        '2C EpCAM Neg': 1.95,
        '>2C': 2.5,
        '<2C EpCAM Pos': 1.5,
        '>2C-4C EpCAM Pos': 2.5,
        '4C EpCAM Pos': 4,
        '2C Rt EpCAM Pos': 2,
        '2C Lt EpCAM Pos': 2,
        '>4C EpCAM Pos': 4,
        '2C EpCAM Pos': 2,
        '>2C EpCAM Pos': 2.5,
        '2C Lt': 1.75,
        '<2C': 1.5,
        '>2C-4C': 3,
        '>2C-4C Lt': 2.75,
        '>2C-4C Rt': 3.25,
        '>4C': 5,

        '2C EpCAM Neg': 2,
        '<2C EpCAM Pos': 1.5,
        '>2C-4C EpCAM Pos': 3,
        '4C EpCAM Pos': 4,
        '2C Rt EpCAM Pos': 2.25,
        '2C Lt EpCAM Pos': 1.75,
        '>4C EpCAM Pos': 5,
        '2C EpCAM Pos': 2,
        '>2C EpCAM Pos': 2.5,
    }

    def make_gate(self, ordering):
        if self.GATE_COLUMN not in self.guide_df.columns:
            self.gate = None
            return

        gate_column_df = self.guide_df.iloc[ordering, :]
        res = list(map(
            lambda g: self.GATE_MAPPING.get(g, 2),
            gate_column_df[self.GATE_COLUMN].values
        ))
        return np.array(res)

    def make_sector(self, ordering):
        if(self.SECTOR_COLUMN not in self.guide_df.columns):
            self.sector = None
        sector_df = self.guide_df[self.SECTOR_COLUMN]
        self._reset_heatmap_color()
        sector = self._make_heatmap_array(sector_df)
        return sector[ordering]

    def make_multiplier(self, ordering):
        data = self.seg_df.iloc[:self.chrom_x_index, 3:]
        multiplier = data.mean().ix[ordering]
        return multiplier.values

    def make_error(self, ordering):
        df_s = self.seg_df.iloc[:self.chrom_x_index, 3:].values
        df_r = self.ratio_df.iloc[:self.chrom_x_index, 3:].values
        return np.sqrt(np.sum(((df_r - df_s) / df_s)**2, axis=0))[ordering]

    @property
    def bar_extent(self):
        if self._bar_extent is None:
            self._bar_extent = (
                0, self.samples * self.interval_length,
                0, 1)
        return self._bar_extent

    def make_sectors_legend(self):
        sectors = self.guide_df[self.SECTOR_COLUMN].unique()
        sectors.sort()

        print(sectors)

        result = []
        for sector in sectors:
            sector_df = self.guide_df[
                self.guide_df[self.SECTOR_COLUMN] == sector]
            pathology = sector_df[self.PATHOLOGY_COLUMN].values[0]
            if not np.all(sector_df[self.PATHOLOGY_COLUMN] == pathology):
                print("single sector '{}'; different pathologies: {}".format(
                    sector,
                    sector_df[self.PATHOLOGY_COLUMN].unique()))
            result.append((sector, str(pathology).strip()))
        return result

# def gate_compare(g1, g2):
#     assert len(g1) >= 2
#     assert len(g2) >= 2
#
#     if g1[0] == '>' or g1[0] == '<':
#         sg1 = g1[1:].strip()
#         sign1 = sg1[0]
#     else:
#         sg1 = g1
#         sign1 = None
#
#     if g2[0] == '>' or g2[0] == '<':
#         sg2 = g2[1:].strip()
#         sign2 = g2[0]
#     else:
#         sg2 = g2
#         sign2 = None
#     assert len(sg1) >= 2
#     assert len(sg2) >= 2
#
#     if sg1[:2] == sg2[:2] and (sign1 or sign2):
#         if sign1 and sign2:
#             if sign1 > sign2:
#                 return 1
#             elif sign1 < sign2:
#                 return -1
#             else:
#                 return 0
#         else:
#             if sign1:
#                 if sign1 == '<':
#                     return -1
#                 elif sign1 == '>':
#                     return 1
#                 assert False
#             elif sign2:
#                 if sign2 == '<':
#                     return 1
#                 elif sign2 == '>':
#                     return -1
#                 assert False
#     if sg1 > sg2:
#         return 1
#     elif sg1 < sg2:
#         return -1
#     else:
#         return 0

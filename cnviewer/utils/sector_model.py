'''
Created on Jan 10, 2017

@author: lubo
'''
import numpy as np


class SectorDataModel(object):

    def __init__(self, model):
        self.model = model
        self.bins, self.samples = self.model.seg_data.shape

    def build_ordering(self):
        ordering = np.vstack((
            self.model.Z['leaves'],
            self.model.guide_df[self.model.SECTOR_COLUMN].values,
        ))
        print(ordering)
        print(ordering.shape)
        res = np.lexsort(ordering, axis=0)
        print(res)
        print(res.shape)

        print(self.model.guide_df[self.model.SECTOR_COLUMN].unique())
        print(len(self.model.guide_df[self.model.SECTOR_COLUMN].unique()))

        print(ordering[:, res])
        return res

    def make(self):
        ordering = self.build_ordering()

        self.column_labels = np.array(self.seg_df.columns[3:])
        self.label_midpoints = (
            np.arange(self.samples) + 0.5) * self.interval_length

        self.heatmap = self.model.make_heatmap(ordering=ordering)
        self.gate = self.model.make_gate(ordering=ordering)
        self.sector = self.model.make_sector(ordering=ordering)
        self.multiplier = self.model.make_multiplier(ordering=ordering)
        self.error = self.model.make_error(ordering=ordering)

    def __getattr__(self, name):
        return getattr(self.model, name)

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
        index = np.array(self.model.Z['leaves'])
        order = np.arange(len(index))

        res = np.lexsort(
            (
                index,
                self.model.guide_df[self.model.SECTOR_COLUMN].values,
            ))
        return order[res]

    def make(self):
        ordering = self.build_ordering()

        self.column_labels = np.array(self.seg_df.columns[3:])[ordering]
        self.label_midpoints = (
            np.arange(self.samples) + 0.5) * self.interval_length

        self.heatmap = self.model.make_heatmap(ordering=ordering)
        self.gate = self.model.make_gate(ordering=ordering)
        self.sector = self.model.make_sector(ordering=ordering)
        self.multiplier = self.model.make_multiplier(ordering=ordering)
        self.error = self.model.make_error(ordering=ordering)

    def __getattr__(self, name):
        return getattr(self.model, name)

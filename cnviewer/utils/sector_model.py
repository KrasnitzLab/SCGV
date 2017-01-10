'''
Created on Jan 10, 2017

@author: lubo
'''
import numpy as np


class SectorDataModel(object):

    def __init__(self, model):
        self.model = model
        self.bins, self.samples = self.model.seg_data.shape

    def make(self):
        ordering = np.array(range(self.model.samples))
        self.heatmap = self.model.make_heatmap(ordering=ordering)
        self.gate = self.model.make_gate(ordering=ordering)
        self.sector = self.model.make_sector(ordering=ordering)
        self.multiplier = self.model.make_multiplier(ordering=ordering)
        self.error = self.model.make_error(ordering=ordering)

    def __getattr__(self, name):
        return getattr(self.model, name)

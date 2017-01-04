'''
Created on Dec 21, 2016

@author: lubo
'''
from views.base import ViewerBase
import matplotlib.pyplot as plt


class GateViewer(ViewerBase):

    def __init__(self, model):
        super(GateViewer, self).__init__(model)
        self.cmap = plt.get_cmap('coolwarm')

    def draw_ploidy(self, ax):
        assert self.model.gate is not None
        ax.imshow(
            [self.model.gate],
            aspect='auto',
            interpolation='nearest',
            cmap=self.cmap,
            extent=self.model.bar_extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Gate"])

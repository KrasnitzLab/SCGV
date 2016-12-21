'''
Created on Dec 21, 2016

@author: lubo
'''
from matplotlib import cm
from views.base import ViewerBase


class MultiplierViewer(ViewerBase):

    def __init__(self, model):
        super(MultiplierViewer, self).__init__(model)

    def draw_multiplier(self, ax):
        assert self.model.multiplier is not None

        ax.imshow(
            [self.model.multiplier],
            aspect='auto',
            interpolation='nearest',
            cmap=cm.coolwarm,  # @UndefinedVariable
            extent=self.model.bar_extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Multiplier"])

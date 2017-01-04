'''
Created on Dec 21, 2016

@author: lubo
'''
# from matplotlib import cm
from views.base import ViewerBase
import matplotlib.pyplot as plt


class MultiplierViewer(ViewerBase):

    def __init__(self, model):
        super(MultiplierViewer, self).__init__(model)

    def draw_multiplier(self, ax):
        assert self.model.multiplier is not None

        ax.imshow(
            [self.model.multiplier],
            aspect='auto',
            interpolation='nearest',
            # cmap=cm.coolwarm,  # @UndefinedVariable
            cmap=plt.get_cmap('seismic'),
            vmin=self.NORMALIZE_MIN,
            vmax=self.NORMALIZE_MAX,
            extent=self.model.bar_extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Multiplier"])

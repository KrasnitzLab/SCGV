'''
Created on Dec 21, 2016

@author: lubo
'''
# from matplotlib import cm
import matplotlib.pyplot as plt
from views.base import ViewerBase


class ErrorViewer(ViewerBase):
    NORMALIZE_ERROR_MIN = 0
    NORMALIZE_ERROR_MAX = 50

    def __init__(self, model):
        super(ErrorViewer, self).__init__(model)

    def draw_error(self, ax):
        if self.model.error is None:
            return

        ax.imshow(
            [self.model.error],
            aspect='auto',
            interpolation='nearest',
            # cmap=cm.coolwarm,  # @UndefinedVariable
            cmap=plt.get_cmap('Greys'),
            # vmin=self.NORMALIZE_ERROR_MIN,
            # vmax=self.NORMALIZE_ERROR_MAX,
            extent=self.model.bar_extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Error"])

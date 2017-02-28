'''
Created on Dec 21, 2016

@author: lubo
'''
# from matplotlib import cm
from views.base import ViewerBase
# import matplotlib.pyplot as plt
from utils.color_map import ColorMap


class MultiplierViewer(ViewerBase):

    def __init__(self, model):
        super(MultiplierViewer, self).__init__(model)
        self.cmap = ColorMap.make_diverging05()

    def draw_multiplier(self, ax):
        if self.model.multiplier is None:
            return

        ax.imshow(
            [self.model.multiplier],
            aspect='auto',
            interpolation='nearest',
            # cmap=cm.coolwarm,  # @UndefinedVariable
            # cmap=plt.get_cmap('seismic'),
            cmap=self.cmap.colors,
            vmin=self.NORMALIZE_MIN,
            vmax=self.NORMALIZE_MAX,
            extent=self.model.bar_extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Multiplier"])

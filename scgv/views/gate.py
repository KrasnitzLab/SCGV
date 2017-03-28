'''
Created on Dec 21, 2016

@author: lubo
'''
from views.base import ViewerBase
# import matplotlib.pyplot as plt
from utils.color_map import ColorMap


class GateViewer(ViewerBase):

    def __init__(self, model):
        super(GateViewer, self).__init__(model)
        # self.cmap = plt.get_cmap('seismic')
        self.cmap = ColorMap.make_diverging05()

    def draw_ploidy(self, ax):
        if self.model.gate is not None:
            ax.imshow(
                [self.model.gate],
                aspect='auto',
                interpolation='nearest',
                cmap=self.cmap.colors,
                vmin=self.NORMALIZE_MIN,
                vmax=self.NORMALIZE_MAX,
                extent=self.model.bar_extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Gate"])

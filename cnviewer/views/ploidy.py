'''
Created on Dec 21, 2016

@author: lubo
'''
from views.base import ViewerBase
from utils.color_map import ColorMap


class PloidyViewer(ViewerBase):

    def __init__(self, model):
        super(PloidyViewer, self).__init__(model)
        self.cmap = ColorMap.make_cmap07()

    def draw_ploidy(self, ax):
        assert self.model.ploidy is not None
        ax.imshow(
            [self.model.ploidy],
            aspect='auto',
            interpolation='nearest',
            cmap=self.cmap.colors,
            norm=self.cmap.norm,
            extent=self.model.bar_extent)
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Ploidy"])

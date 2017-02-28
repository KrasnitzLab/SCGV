'''
Created on Dec 15, 2016

@author: lubo
'''
from views.base import ViewerBase
from utils.color_map import ColorMap


class SectorViewer(ViewerBase):

    def __init__(self, model):
        super(SectorViewer, self).__init__(model)
        self.cmap = ColorMap.make_qualitative12()

    def draw_sector(self, ax):
        if self.model.sector is None:
            return

        ax.imshow(
            [self.model.sector],
            aspect='auto',
            interpolation='nearest',
            cmap=self.cmap.colors,
            vmin=1,
            vmax=12,
            # norm=self.cmap.norm,
            extent=self.model.bar_extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels(["Sector"])

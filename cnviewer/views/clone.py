'''
Created on Dec 15, 2016

@author: lubo
'''
from views.base import ViewerBase
from utils.color_map import ColorMap


class CloneViewer(ViewerBase):

    def __init__(self, model):
        super(CloneViewer, self).__init__(model)
        self.cmap = ColorMap.make_cmap07()

    def draw_clone(self, ax):
        assert self.model.clone is not None
        assert self.model.subclone is not None

        ax.imshow(
            [self.model.clone],
            aspect='auto',
            interpolation='nearest',
            cmap=self.cmap.colors,
            norm=self.cmap.norm,
            extent=self.model.bar_extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.0])
        ax.set_yticklabels(["Clone"])

    def draw_subclone(self, ax):
        assert self.model.clone is not None
        assert self.model.subclone is not None

        ax.imshow(
            [self.model.subclone],
            aspect='auto',
            interpolation='nearest',
            cmap=self.cmap.colors,
            norm=self.cmap.norm,
            extent=self.model.bar_extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_yticklabels([])

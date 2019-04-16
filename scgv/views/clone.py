'''
Created on Dec 15, 2016

@author: lubo
'''
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scgv.views.base import ViewerBase


class CloneViewer(ViewerBase):

    def __init__(self, model):
        super(CloneViewer, self).__init__(model)
        self._select_colormap()

    def _select_colormap_size(self, size):
        assert size <= 20
        if size > 12:
            cmap = plt.get_cmap('tab20')
        elif size > 7:
            cmap = plt.get_cmap('Paired')
        else:
            cmap = plt.get_cmap('tab10')
        colors = ['#FFFFFF']
        colors.extend(cmap.colors[:size])
        return ListedColormap(colors)

    def _select_colormap(self):
        self.vmax = np.max(self.model.subclone)
        size = int(self.vmax)
        self.cmap = self._select_colormap_size(size)

    def draw_clone(self, ax):

        if self.model.clone is not None:
            ax.imshow(
                [self.model.clone],
                aspect='auto',
                interpolation='nearest',
                cmap=self.cmap,
                # norm=self.cmap.norm,
                vmin=0,
                vmax=self.vmax,
                extent=self.model.bar_extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.0])
        ax.set_yticklabels(["Clone"])

    def draw_subclone(self, ax):
        if self.model.subclone is not None:
            ax.imshow(
                [self.model.subclone],
                aspect='auto',
                interpolation='nearest',
                cmap=self.cmap,
                vmin=0,
                vmax=self.vmax,
                extent=self.model.bar_extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_yticklabels([])

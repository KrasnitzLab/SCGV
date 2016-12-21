'''
Created on Dec 14, 2016

@author: lubo
'''

import numpy as np
from views.base import ViewerBase


class DendrogramViewer(ViewerBase):

    def __init__(self, model):
        super(DendrogramViewer, self).__init__(model)

    def _draw_dendrogram(self, ax):
        assert self.model.Z is not None

        dcoord = self.model.dcoord
        max_dcoord = np.max(dcoord)
        dcoord_hang = 0.1 * max_dcoord

        ys = dcoord[:, 1] - dcoord_hang
        ys[ys < 0] = 0
        zeros = dcoord[:, 0] == 0
        dcoord[zeros, 0] = ys[zeros]

        ys = dcoord[:, 2] - dcoord_hang
        ys[ys < 0] = 0
        zeros = dcoord[:, 3] == 0
        dcoord[zeros, 3] = ys[zeros]

        icoord = self.model.icoord
        color_list = np.array(self.model.Z['color_list'])

        min_x = np.min(icoord)
        max_x = np.max(icoord)

        min_y = np.min(dcoord)
        max_y = np.max(dcoord)

        for xs, ys, color in zip(icoord, dcoord, color_list):
            ax.plot(xs, ys, color)
        ax.set_xlim(min_x - 10, max_x + 10)
        ax.set_ylim(min_y, max_y + 0.05 * max_y)

    def draw_dendrogram(self, ax):
        self._draw_dendrogram(ax)
        self.clear_xlabels(ax)
        self.draw_ylabels(ax)

    def clear_xlabels(self, ax):
        ax.set_xticks(self.model.label_midpoints)
        ax.set_xticklabels([''] * len(self.model.column_labels))

    def draw_xlabels(self, ax):
        ax.set_xticks(self.model.label_midpoints)
        ax.set_xticklabels(self.model.column_labels,
                           rotation='vertical',
                           fontsize=10)

    def draw_ylabels(self, ax):
        max_y = np.max(self.model.Z['dcoord'])
        yticks = np.array([0, 0.25, 0.5, 0.75, 1.0]) * max_y
        ylabels = ["{:.0f}".format(np.round(y)) for y in yticks]

        ax.set_yticks(max_y - yticks)
        ax.set_yticklabels(ylabels)

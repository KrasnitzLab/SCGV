import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from scgv.views.base import ViewerBase
# from scgv.utils.color_map import ColorMap


class TrackViewer(ViewerBase):

    @classmethod
    def select_colormap(self, track_mapping):
        size = len(track_mapping)

        assert size <= 20
        if size > 12:
            print("select_colormap: tab20")
            cmap = plt.get_cmap('tab20')
        elif size > 7:
            print("select_colormap: Paired")
            cmap = plt.get_cmap('Paired')
        else:
            print("select_colormap: tab10")
            cmap = plt.get_cmap('tab10')

        return ListedColormap(cmap.colors[:size])

    def __init__(self, model, track_name, track, mapping):
        super(TrackViewer, self).__init__(model)

        self.track_name = track_name
        self.track = track
        self.track_mapping = mapping

    def draw(self, ax):
        if self.track is not None:

            cmap = self.select_colormap(self.track_mapping)
            vmin = np.min(self.track)
            track = self.track - vmin
            vmin = np.min(track)
            vmax = np.max(track)

            ax.imshow(
                [track],
                aspect='auto',
                interpolation='nearest',
                cmap=cmap,
                vmin=vmin,
                vmax=vmax,
                extent=self.model.bar_extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels([self.track_name])

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from scgv.views.base import ViewerBase
# from scgv.utils.color_map import ColorMap


class TrackViewer(ViewerBase):

    @classmethod
    def select_colormap(self, track_mapping):
        size = len(track_mapping)
        return TrackViewer.select_colormap_size(size)

    @classmethod
    def select_colormap_size(self, size):
        assert size <= 20
        if size > 12:
            cmap = plt.get_cmap('tab20')
        elif size > 7:
            cmap = plt.get_cmap('Paired')
        else:
            cmap = plt.get_cmap('tab10')
        colors = cmap.colors[:size]
        return ListedColormap(colors)

    def __init__(self, model, track_name, track, mapping):
        super(TrackViewer, self).__init__(model)

        self.track_name = track_name
        self.track = track
        self.track_mapping = mapping

    def draw(self, ax):
        if self.track is not None:

            cmap = self.select_colormap(self.track_mapping)
            vmin = min(self.track_mapping.values())
            vmax = max(self.track_mapping.values())
            track = self.track - vmin

            ax.imshow(
                [track],
                aspect='auto',
                interpolation='nearest',
                cmap=cmap,
                vmin=0,
                vmax=vmax - vmin,
                extent=self.model.bar_extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels([self.track_name])

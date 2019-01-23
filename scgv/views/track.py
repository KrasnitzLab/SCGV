import matplotlib.pyplot as plt

from scgv.views.base import ViewerBase
# from scgv.utils.color_map import ColorMap


class TrackViewer(ViewerBase):

    def select_colormap(self):
        size = len(self.track_mapping)

        assert size <= 20
        if size > 12:
            return plt.get_cmap('tab20')
        elif size > 10:
            return plt.get_cmap('Paired')
        else:
            return plt.get_cmap('tab10')

    def __init__(self, model, track_name, track, mapping):
        super(TrackViewer, self).__init__(model)

        self.track_name = track_name
        self.track = track
        self.track_mapping = mapping

    def draw_track(self, ax):
        if self.track is not None:

            cmap = self.select_colormap()
            ax.imshow(
                [self.track],
                aspect='auto',
                interpolation='nearest',
                cmap=cmap,
                vmin=1,
                vmax=12,
                extent=self.model.bar_extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels([self.track_name])

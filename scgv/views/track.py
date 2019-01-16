from scgv.views.base import ViewerBase
from scgv.utils.color_map import ColorMap


class TrackViewer(ViewerBase):

    def __init__(self, model, track_name):
        super(TrackViewer, self).__init__(model)

        self.cmap = ColorMap.make_qualitative12()
        self.track_name = track_name
        self.track, self.track_mapping = \
            self.model.make_track(track_name, self.model.ordering)

    def draw_track(self, ax):
        if self.model.sector is not None:
            ax.imshow(
                [self.track],
                aspect='auto',
                interpolation='nearest',
                cmap=self.cmap.colors,
                vmin=1,
                vmax=12,
                extent=self.model.bar_extent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0.5])
        ax.set_yticklabels([self.track_name])

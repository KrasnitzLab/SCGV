'''
Created on Dec 14, 2016

@author: lubo
'''
from views.sample import SampleViewer
from views.heatmap import HeatmapViewer
from views.dendrogram import DendrogramViewer
from views.clone import CloneViewer
from views.ploidy import PloidyViewer
from views.multiplier import MultiplierViewer
from views.error import ErrorViewer


class ControllerBase(object):

    def __init__(self, model):
        self.model = model

    @staticmethod
    def debug_event(event):
        # print(event)
        if event.name == 'button_press_event':
            print("MOUSE: name={}; xy=({},{}); xydata=({},{}); "
                  "button={}; dblclick={}".format(
                      event.name,
                      event.x, event.y,
                      event.xdata, event.ydata,
                      event.button, event.dblclick
                  ))
        elif event.name == 'key_press_event':
            print("KEY: name={}; xy=({},{}); xydata=({},{}); "
                  "key={}".format(
                      event.name,
                      event.x, event.y,
                      event.xdata, event.ydata,
                      event.key
                  ))
        else:
            print("???: {}".format(event.name))


class MainController(ControllerBase):

    def __init__(self, model):
        super(MainController, self).__init__(model)
        self.sample_viewer = None
        self.sample_list = []
        self.fig = None

    def event_loop_connect(self):
        self.fig.canvas.mpl_connect('button_press_event', self.event_handler)
        self.fig.canvas.mpl_connect('key_press_event', self.event_handler)

    def event_handler(self, event):
        print("event tester called...")
        self.debug_event(event)
        if event.name == 'button_press_event':
            sample = self.locate_sample_click(event)
            self.add_sample(sample)
        elif event.name == 'key_press_event' and event.key == 'd':
            print(self.sample_list)

            self.display_samples()
            self.sample_list = []

    def add_sample(self, sample):
        if sample is None:
            return
        if sample in self.sample_list:
            return
        self.sample_list.append(sample)

    def display_samples(self):
        self.sample_viewer.draw_samples(self.sample_list)

    def locate_sample_click(self, event):
        if event.xdata is None:
            return None
        xloc = int(event.xdata / self.model.interval_length)
        sample_name = self.model.column_labels[xloc]
        print("xloc: {}; sample name: {}".format(xloc, sample_name))
        return sample_name

    def build_main(self, fig):
        assert self.fig is None
        self.fig = fig

        ax_dendro = fig.add_axes([0.1, 0.775, 0.8, 0.175], frame_on=True)
        dendro_viewer = DendrogramViewer(self.model)
        dendro_viewer.draw_dendrogram(ax_dendro)

        clone_viewer = CloneViewer(self.model)
        ax_clone = fig.add_axes(
            [0.1, 0.7625, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer.draw_clone(ax_clone)
        ax_subclone = fig.add_axes(
            [0.1, 0.75, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer.draw_subclone(ax_subclone)

        heatmap_viewer = HeatmapViewer(self.model)
        ax_heat = fig.add_axes(
            [0.1, 0.20, 0.8, 0.55], frame_on=True, sharex=ax_dendro)
        heatmap_viewer.draw_heatmap(ax_heat)
        heatmap_viewer.draw_legend()

        ax_sector = fig.add_axes(
            [0.1, 0.175, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        # draw sector bar
        ax_sector.set_xticks([])
        ax_sector.set_xticklabels([])
        ax_sector.set_yticks([0.5])
        ax_sector.set_yticklabels(["Sector"])

        ax_ploidy = fig.add_axes(
            [0.1, 0.150, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        ploidy_viewer = PloidyViewer(self.model)
        ploidy_viewer.draw_ploidy(ax_ploidy)

        ax_multiplier = fig.add_axes(
            [0.1, 0.125, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        multiplier_viewer = MultiplierViewer(self.model)
        multiplier_viewer.draw_multiplier(ax_multiplier)

        ax_error = fig.add_axes(
            [0.1, 0.10, 0.8, 0.025], frame_on=True)  # , sharex=ax_dendro)
        error_viewer = ErrorViewer(self.model)
        error_viewer.draw_error(ax_error)

        error_viewer.draw_xlabels(ax_error)

        self.sample_viewer = SampleViewer(self.model)
        self.event_loop_connect()

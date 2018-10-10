'''
Created on Jan 18, 2017

@author: lubo
'''

from scgv.tkviews.canvas_window import CanvasWindow
from scgv.views.sample import SamplesViewer


class SamplesWindow(object):

    def __init__(self, master, controller, samples):
        self.master = master
        self.controller = controller
        self.samples = samples[:]

    def build_ui(self):
        self.main = CanvasWindow(self.master, self.controller, legend=False)

    def draw_canvas(self):
        samples_viewer = SamplesViewer(self.controller.model)
        samples_viewer.draw_samples(self.main.fig, self.samples)

        self.controller.event_loop_connect(self.main.fig)

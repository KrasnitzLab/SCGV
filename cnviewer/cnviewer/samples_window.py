'''
Created on Jan 18, 2017

@author: lubo
'''

from tkutils.tkimport import *  # @UnusedWildImport

from tkutils.canvas_ui import CanvasWindow
from views.sample import SamplesViewer


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

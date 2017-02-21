'''
Created on Jan 18, 2017

@author: lubo
'''

from tkutils.tkimport import *  # @UnusedWildImport

from tkutils.canvas_ui import CanvasWindow


class SampleWindow(object):

    def __init__(self, master, controller, sample_list):
        self.master = master
        self.controller = controller
        self.sample_list = sample_list[:]

    def build_ui(self):
        self.main = CanvasWindow(self.root, legend=False)
        return self.main.fig

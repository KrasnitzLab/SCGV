'''
Created on Jan 18, 2017

@author: lubo
'''

from tkutils.tkimport import *  # @UnusedWildImport

from tkutils.canvas_ui import CanvasWindow


class SampleUi(object):

    def __init__(self, sample_list):
        self.root = tk.Toplevel()
        self.sample_list = sample_list[:]

    def build_ui(self):
        self.main = CanvasWindow(self.root, legend=False)
        return self.main.fig

    def mainloop(self):
        self.root.mainloop()

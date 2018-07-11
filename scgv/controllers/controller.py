'''
Created on Dec 14, 2016

@author: lubo
'''

import webbrowser

from scgv.controllers.controller_base import HeatmapControllerBase, \
    ControllerBase
from scgv.models.model import DataModel
import numpy as np


class SamplesController(ControllerBase):

    def __init__(self, model):
        super(SamplesController, self).__init__()
        self.model = model
        self.start_pos = None
        self.end_pos = None

    def event_handler(self, event):
        print("event_handler called...")
        self.debug_event(event)
        if event.name == 'button_press_event' and event.button == 3:
            pos = self.translate_xcoord(event.xdata)
            if self.start_pos is None:
                self.start_pos = pos
            else:
                self.end_pos = pos
                self.open_genome_browser()

    def translate_xcoord(self, xdata):
        index = np.abs(self.model.data.seg_df.abspos.values - xdata).argmin()
        chrom, chrompos = self.model.data.seg_df.iloc[index, [0, 1]]
        return (int(chrom), int(chrompos))

    def open_genome_browser(self):
        if self.start_pos is None or self.end_pos is None:
            return
        if self.start_pos[0] != self.end_pos[0]:
            self.start_pos = None
            self.end_pos = None
            return
        chrom = self.start_pos[0]
        if chrom == 23:
            chrom = 'X'
        if chrom == 24:
            chrom = 'Y'
        position = 'chr{}:{}-{}'.format(
            chrom, self.start_pos[1], self.end_pos[1])
        genome = self.model.data.genome
        assert genome is not None

        url = "http://genome.ucsc.edu/cgi-bin/hgTracks?db={}&position={}"\
            .format(genome, position)
        print('opening url: ', url)
        webbrowser.open(url, new=False, autoraise=True)
        self.start_pos = None
        self.end_pos = None


class SectorsController(HeatmapControllerBase):

    def __init__(self, model):
        super(SectorsController, self).__init__()
        self.model = model


class FeaturematController(HeatmapControllerBase):

    def __init__(self, model):
        super(FeaturematController, self).__init__()
        self.model = model


class SingleSectorController(HeatmapControllerBase):

    def __init__(self, model):
        super(SingleSectorController, self).__init__()
        self.model = model


class MainController(HeatmapControllerBase):

    def __init__(self):
        super(MainController, self).__init__()
        self.sample_viewer = None
        self.model = None
        self.on_model_callbacks = []

        self.add_sample_cb = None
        self.ax_label = None

    def register_on_model_callback(self, cb):
        self.on_model_callbacks.append(cb)

    def load_model(self, filename):
        self.filename = filename
        self.model = DataModel(self.filename)
        self.model.make()
        return self.model

    def reset_model(self):
        self.model = None

    def trigger_on_model_callbacks(self):
        for cb in self.on_model_callbacks:
            cb(self.model)
        return self.model

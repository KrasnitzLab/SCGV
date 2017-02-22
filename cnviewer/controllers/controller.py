'''
Created on Dec 14, 2016

@author: lubo
'''

from controllers.controller_base import HitmapControllerBase, ControllerBase
from models.model import DataModel


class SamplesController(ControllerBase):

    def __init__(self, model):
        super(SamplesController, self).__init__()
        self.model = model


class SectorsController(HitmapControllerBase):

    def __init__(self, model):
        super(SectorsController, self).__init__()
        self.model = model


class PinmatController(HitmapControllerBase):

    def __init__(self, model):
        super(PinmatController, self).__init__()
        self.model = model


class MainController(HitmapControllerBase):

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

    def trigger_on_model_callbacks(self):
        for cb in self.on_model_callbacks:
            cb(self.model)
        return self.model

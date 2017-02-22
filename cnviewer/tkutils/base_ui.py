'''
Created on Feb 22, 2017

@author: lubo
'''


class BaseUi(object):

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

    def enable_ui(self):
        raise NotImplemented()

    def disable_ui(self):
        raise NotImplemented()

    def on_model(self, model):
        self.model = model
        self.enable_ui()

    def build_ui(self):
        self.connect_controller()

    def connect_controller(self):
        if self.controller.model is None:
            self.controller.register_on_model_callback(self.on_model)
        else:
            self.on_model(self.controller.model)

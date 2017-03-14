'''
Created on Feb 22, 2017

@author: lubo
'''
from utils.observer import DataObserver


class BaseUi(DataObserver):

    def __init__(self, master, controller, subject):
        super(BaseUi, self).__init__(subject)
        self.master = master
        self.controller = controller

    def enable_ui(self):
        raise NotImplemented()

    def disable_ui(self):
        raise NotImplemented()

    def update(self):
        self.model = self.get_model()
        self.enable_ui()

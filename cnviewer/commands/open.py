'''
Created on Mar 13, 2017

@author: lubo
'''
import os
import threading
import traceback

from models.model import DataModel


class OpenCommand(object):
    DELAY = 500

    def __init__(self, master, subject, filename):
        assert subject.model is None
        assert os.path.exists(filename)

        self.filename = filename
        self.subject = subject
        self.master = master

    def execute(self):
        self.task = threading.Thread(target=self.run, args=[self])
        self.task.start()

    def run(self, *args):
        try:
            model = DataModel(self.filename)
            model.make()
            self.set_model(model)
        except Exception:
            print("wrong dataset format")
            traceback.print_exc()
            model = None
            self.set_model(None)

    def set_model(self, model):
        def model_setter(*args):
            self.subject.set_model(model)

        self.master.after(self.DELAY, model_setter, self)

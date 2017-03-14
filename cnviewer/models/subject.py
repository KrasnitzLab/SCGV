'''
Created on Mar 14, 2017

@author: lubo
'''


class DataSubject(object):

    def __init__(self):
        self.model = None
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        pass

    def set_model(self, model):
        self.model = model
        self.notify()

    def notify(self):
        for observer in self.observers:
            observer.update()

    def get_model(self):
        return self.model

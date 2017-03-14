'''
Created on Mar 14, 2017

@author: lubo
'''


class Observer(object):

    def __init__(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def update(self):
        raise NotImplemented()

    def get_subject(self):
        return self.subject

    def get_model(self):
        return self.subject.model

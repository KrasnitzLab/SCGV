'''
Created on Feb 28, 2017

@author: lubo
'''


class ModelDelegate(object):

    def __init__(self, model):
        self.model = model

    def __getattr__(self, name):
        return getattr(self.model, name)

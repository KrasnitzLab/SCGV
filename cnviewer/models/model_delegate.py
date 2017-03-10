'''
Created on Feb 28, 2017

@author: lubo
'''
# import traceback


class ModelDelegate(object):

    def __init__(self, model):
        self.model = model

    def __getattr__(self, name):
        print("getattr: ", name, type(getattr(self.model, name)))
        # traceback.print_stack(limit=5)
        return getattr(self.model, name)

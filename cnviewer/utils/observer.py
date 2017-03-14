'''
Created on Mar 14, 2017

@author: lubo
'''


class Observer(object):

    def __init__(self, subject):
        self.subject = subject

    def update(self):
        raise NotImplemented()

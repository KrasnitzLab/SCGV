'''
Created on Mar 14, 2017

@author: lubo
'''


class DataObserver(object):

    def __init__(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def update(self, subject):
        raise NotImplemented()

    def get_subject(self):
        return self.subject

    def get_model(self):
        return self.subject.model


class ProfilesObserver(object):

    def __init__(self, profiles_subject):
        self.profiles_subject = profiles_subject
        self.profiles_subject.register_observer(self)

    def update(self, subject):
        raise NotImplemented()

    def get_profiles(self):
        return self.profiles_subject

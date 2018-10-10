'''
Created on Mar 14, 2017

@author: lubo
'''
import traceback
from scgv.utils.observer import ProfilesObserver, DataObserver


class DataSubject(object):

    def __init__(self):
        self.model = None
        self.observers = []

    def register_observer(self, observer):
        assert isinstance(observer, DataObserver)
        self.observers.append(observer)

    def remove_observer(self, observer):
        pass

    def set_model(self, model):
        self.model = model
        self.notify()

    def notify(self):
        for observer in self.observers:
            try:
                observer.update(self)
            except Exception:
                print("unexpected exception during notify...")
                traceback.print_exc()

    def get_model(self):
        return self.model


class ProfilesSubject(object):

    def __init__(self):
        self.available_profiles = []
        self.removed_profiles = []

        self.profile_observers = []

    def register_observer(self, observer):
        assert isinstance(observer, ProfilesObserver)
        self.profile_observers.append(observer)

    def notify_profiles(self):

        for observer in self.profile_observers:
            try:
                observer.update(self)
            except Exception:
                print("unexpected exception during notify...")
                traceback.print_exc()

    def get_available_profiles(self):
        return self.available_profiles

    def get_removed_profiles(self):
        return self.removed_profiles

    def add_profiles(self, profiles):
        self.available_profiles.extend(profiles)
        self.available_profiles = list(set(self.available_profiles))

        self.removed_profiles = []
        self.notify_profiles()

    def clear_profiles(self):
        self.removed_profiles = self.available_profiles[:]
        self.available_profiles = []
        self.notify_profiles()

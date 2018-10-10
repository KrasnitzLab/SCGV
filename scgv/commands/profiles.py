'''
Created on Mar 14, 2017

@author: lubo
'''
import tkinter as tk


from scgv.commands.command import Command
from scgv.controllers.controller import SamplesController
from scgv.tkviews.samples_window import SamplesWindow


class ShowProfilesCommand(Command):

    def __init__(self, model, profiles_subject):
        self.model = model
        self.profiles_subject = profiles_subject

    def execute(self):
        profiles = self.profiles_subject.get_available_profiles()
        if not profiles:
            return

        self.profiles_subject.clear_profiles()

        root = tk.Toplevel()
        controller = SamplesController(self.model)
        samples_window = SamplesWindow(root, controller, profiles)
        samples_window.build_ui()
        samples_window.draw_canvas()
        root.mainloop()


class ClearProfilesCommand(Command):

    def __init__(self, profiles_subject):
        self.profiles_subject = profiles_subject

    def execute(self):
        self.profiles_subject.clear_profiles()


class AddProfilesCommand(Command):

    def __init__(self, profiles_subject, profiles):
        self.profiles_subject = profiles_subject
        self.profiles = profiles

    def execute(self):
        self.profiles_subject.add_profiles(self.profiles)

'''
Created on Mar 14, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport


from commands.command import Command
from controllers.controller import SamplesController
from tkviews.samples_window import SamplesWindow


class ShowProfilesCommand(Command):

    def __init__(self, model, samples):
        self.model = model
        self.samples = samples

    def execute(self):
        root = tk.Toplevel()
        controller = SamplesController(self.model)
        samples_window = SamplesWindow(root, controller, self.samples)
        samples_window.build_ui()
        samples_window.draw_canvas()
        root.mainloop()


class ClearProfilesCommand(Command):

    def __init__(self, master, profiles_box):
        self.master = master
        self.profiles_box = profiles_box

    def execute(self):
        profiles = self.profiles_box.get(0, 'end')
        self.profiles_box.delete(0, 'end')
        self.master.unhighlight_profile_labels(profiles)


class AddProfilesCommand(Command):

    def __init__(self, master, profiles_box, profiles):
        self.master = master
        self.profiles_box = profiles_box
        self.profiles = profiles

    def execute(self):
        for profile in self.profiles:
            profiles = self.profile_ui.get(0, 'end')
            if profile in profiles:
                continue
            self.profile_ui.insert("end", profile)
        profiles = self.profile_ui.get(0, 'end')
        self.master.highlight_profiles_labels(profiles)

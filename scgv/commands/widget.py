'''
Created on Mar 14, 2017

@author: lubo
'''
from scgv.tkviews.tkimport import *  # @UnusedWildImport
from scgv.commands.command import Command


class DisableCommand(Command):

    def __init__(self, *args):
        self.widgets = args[:]

    def execute(self):
        for widget in self.widgets:
            widget.config(state=tk.DISABLED)


class EnableCommand(Command):

    def __init__(self, *args):
        self.widgets = args[:]

    def execute(self):
        for widget in self.widgets:
            widget.config(state=tk.ACTIVE)

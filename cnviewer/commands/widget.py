'''
Created on Mar 14, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport
from commands.command import Command


class DisableCommand(Command):

    def __init__(self, widget):
        self.widget = widget

    def execute(self):
        self.widget.config(state=tk.DISABLED)


class EnableCommand(Command):

    def __init__(self, widget):
        self.widget = widget

    def execute(self):
        self.widget.config(state=tk.ACTIVE)

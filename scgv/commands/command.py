'''
Created on Mar 14, 2017

@author: lubo
'''


class Command(object):

    def __init__(self, *args):
        pass

    def execute(self):
        raise NotImplemented()


class MacroCommand(Command):

    def __init__(self, *args):
        assert all([isinstance(c, Command) for c in args])
        self.commands = args[:]

    def add_command(self, command):
        assert isinstance(command, Command)
        self.commands.append(command)

    def execute(self):
        for command in self.commands:
            command.execute()

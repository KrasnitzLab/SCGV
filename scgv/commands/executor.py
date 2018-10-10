'''
Created on Mar 14, 2017

@author: lubo
'''

from scgv.commands.command import Command
import queue  # @UnusedImport @UnresolvedImport @NoMove @Reimport


class CommandExecutor(object):
    DELAY = 100
    EXECUTOR = None

    def __init__(self, root):
        self.root = root
        self.queue = queue.Queue()

    def run(self, *args):
        if not self.queue.empty():
            try:
                command = self.queue.get_nowait()
            except queue.Empty:
                command = None
            if command is not None:
                command.execute()
        self.root.after(self.DELAY, self.run, self)

    @classmethod
    def get(cls):
        return cls.EXECUTOR

    @classmethod
    def start(cls, root):
        if cls.EXECUTOR is None:
            cls.EXECUTOR = CommandExecutor(root)
        cls.EXECUTOR.run()

    @classmethod
    def execute(cls, command, master):
        assert isinstance(command, Command)

        def do_command():
            command.execute()

        master.after_idle(do_command)

    @classmethod
    def execute_after(cls, command):
        assert isinstance(command, Command)
        cls.EXECUTOR.queue.put(command)

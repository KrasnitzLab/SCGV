'''
Created on Jan 16, 2017

@author: lubo
'''
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import matplotlib as mpl
from scgv.models.subject import DataSubject, ProfilesSubject
from scgv.commands.executor import CommandExecutor
import os
import traceback
mpl.use('TkAgg')

from scgv.tkviews.tkimport import *  # @UnusedWildImport @NoMove @IgnorePep8

# from models.sector_model import SingleSectorDataModel
from scgv.controllers.controller import MainController  # @IgnorePep8
from scgv.tkviews.main_window import MainWindow  # @IgnorePep8


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):

        return self.msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    else:
        argv.extend(sys.argv)

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = "SCGV is an interacive graphical tool for " \
        "single-cell genomics data, with emphasis on single-cell " \
        "genomics of cancer"
    program_description = '''%s

USAGE
''' % (program_shortdesc, )
    program_version_message = "1.0.3"
    try:

        parser = ArgumentParser(
            description=program_description,
            formatter_class=RawDescriptionHelpFormatter)

        parser.add_argument(
            '-V', '--version',
            action='version', version=program_version_message)

        args = parser.parse_args()
        print(args)

        root = tk.Tk()
        root.wm_title("SCGV")

        CommandExecutor.start(root)

        data_subject = DataSubject()
        profiles_subject = ProfilesSubject()

        controller = MainController()
        main = MainWindow(
            root, controller, data_subject, profiles_subject)
        main.build_ui()

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        root.mainloop()

        return 0
    except KeyboardInterrupt:
        traceback.print_exc()
        return 0
    except Exception as e:
        traceback.print_exc()

        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        sys.stderr.write('\n')
        return 2


if __name__ == "__main__":
    main()

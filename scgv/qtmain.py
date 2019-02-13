from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import sys

import scgv.qtviews.mpl_backend  # noqa

from PyQt5.QtWidgets import QApplication

from scgv.qtviews.main_window import MainWindow

import os
import traceback


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

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()

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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject, pyqtSignal


class CloseSignals(QObject):
    closing = pyqtSignal()


class BaseDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(BaseDialog, self).__init__(*args, **kwargs)
        self.signals = CloseSignals()

    def closeEvent(self, event):
        print("closing window...")
        self.signals.closing.emit()

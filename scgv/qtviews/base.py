from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject, pyqtSignal


class CloseSignals(QObject):
    closing = pyqtSignal()


class BaseDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(BaseDialog, self).__init__(*args, **kwargs)
        # self.setWindowFlags(
        #     self.windowFlags() |
        #     Qt.CustomizeWindowHint |
        #     Qt.WindowMaximizeButtonHint |
        #     Qt.WindowType_Mask)
        self.signals = CloseSignals()
        print(self.sizeHint())
        # self.resize(self.sizeHint())

    def closeEvent(self, event):
        print("closing window...")
        self.signals.closing.emit()

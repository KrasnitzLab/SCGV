from PyQt5.QtWidgets import QHBoxLayout, \
    QDialog, QLabel, QTextEdit

from PyQt5.QtGui import QPixmap, QImage, QTextDocument


class ShowPathologyWindow(QDialog):

    def __init__(self, image, notes, parent, *args, **kwargs):
        super(ShowPathologyWindow, self).__init__(parent, *args, **kwargs)
        qimage = QImage()
        qimage.loadFromData(image)
        self.image = QPixmap.fromImage(qimage)
        self.notes = notes

        label = QLabel(self)
        label.setPixmap(self.image)

        text = QTextEdit(self)
        text.setReadOnly(True)

        doc = QTextDocument()
        doc.setPlainText("".join(notes))
        text.setDocument(doc)

        layout = QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(text)

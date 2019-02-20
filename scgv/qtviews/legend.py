from PyQt5.QtWidgets import QWidget, QVBoxLayout, \
    QListWidget, QListWidgetItem, QMenu

from PyQt5.QtGui import QIcon, QPixmap, \
    QPainter, QColor
from PyQt5.QtCore import Qt

import matplotlib.colors as col

from scgv.utils.color_map import ColorMap


class LegendWidget(QWidget):
    IMAGE_SIZE = 15

    def __init__(self, main, *args, **kwargs):
        super(LegendWidget, self).__init__(*args, **kwargs)
        self.main = main
        self.context_menu_actions = None

        layout = QVBoxLayout(self)
        self.list = QListWidget(self)
        layout.addWidget(self.list)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def set_context_menu_actions(self, context_menu_actions):
        self.context_menu_actions = context_menu_actions

    def on_context_menu(self, pos, *args, **kwargs):
        if not self.context_menu_actions:
            return
        current_row = self.list.currentRow()
        if current_row < 0:
            return

        context = QMenu(self.list)
        for action in self.context_menu_actions:
            context.addAction(action)
        context.exec_(self.mapToGlobal(pos))

    @staticmethod
    def qcolor(color):
        if isinstance(color, tuple):
            c = color
        else:
            c = col.to_rgba(color)

        if len(c) == 3:
            r, g, b = color
            a = 1
        elif len(c) == 4:
            r, g, b, a = color
        else:
            raise ValueError("strange color: {}".format(str(color)))
        return QColor(int(255 * r), int(255 * g), int(255 * b), int(255 * a))

    def color_icon(self, color):
        color = self.qcolor(color)
        image = QPixmap(self.IMAGE_SIZE, self.IMAGE_SIZE)
        painter = QPainter(image)
        painter.fillRect(image.rect(), color)
        painter.end()
        return QIcon(image)

    def add_entry(self, text, color):
        icon = self.color_icon(color)
        item = QListWidgetItem(icon, text, self.list)
        self.list.addItem(item)

    def show(self):
        pass

    def clear(self):
        self.list.clear()

    def set_model(self, model):
        self.model = model
        self.show()


class HeatmapLegend(LegendWidget):

    COPYNUM_LABELS = [
        "    0", "    1", "    2", "    3", "    4+"
    ]

    def __init__(self, main, *args, **kwargs):
        super(HeatmapLegend, self).__init__(main, *args, **kwargs)

    def show(self):
        cmap = ColorMap.make_diverging05()
        for index, label in enumerate(self.COPYNUM_LABELS):
            color = cmap.colors(index)
            self.add_entry(label, color)

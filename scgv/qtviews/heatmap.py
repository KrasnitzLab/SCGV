import pandas as pd
from functools import partial
from collections import defaultdict

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QDialog, \
    QPushButton
from PyQt5.QtWidgets import QAction, QListWidget, QListWidgetItem, QMenu, \
    QTableWidget, QTableWidgetItem, QCheckBox

from PyQt5.QtGui import QIcon, QPixmap, \
    QPainter, QColor
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QObject, pyqtSignal

import matplotlib.colors as col

from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar

from scgv.qtviews.canvas import Canvas
from scgv.qtviews.profiles import ProfilesActions


from scgv.utils.color_map import ColorMap
from scgv.models.sector_model import SingleSectorDataModel
from scgv.qtviews.pathology_window import ShowPathologyWindow


class CloseSignals(QObject):
    closing = pyqtSignal()


class LegendWidget(QWidget):
    IMAGE_SIZE = 15

    def __init__(self, main, *args, **kwargs):
        super(LegendWidget, self).__init__(*args, **kwargs)
        self.main = main

        layout = QVBoxLayout(self)
        self.list = QListWidget(self)
        layout.addWidget(self.list)

    @staticmethod
    def qcolor(color):
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
        raise NotImplementedError()

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


class SectorsLegend(LegendWidget):

    def __init__(self, main, *args, **kwargs):
        super(SectorsLegend, self).__init__(main, *args, **kwargs)
        self.sectors = None

    def show(self):
        assert self.model is not None

        if self.sectors is None:
            self.sectors = self.model.make_sectors_legend()
        if self.sectors is None:
            return

        self.cmap = ColorMap.make_qualitative12()

        for (index, (sector, pathology)) in enumerate(self.sectors):
            color = self.cmap.colors(index)
            self.add_entry(
                text=pathology,
                color=color)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, pos, *args, **kwargs):
        show_sector_view = QAction("Show sector view", self)
        show_sector_view.triggered.connect(self.show_sector_view)
        show_pathology_view = QAction("Show sector pathology", self)
        show_pathology_view.triggered.connect(self.show_pathology_view)

        context = QMenu(self)
        context.addAction(show_sector_view)
        if self.model.pathology:
            context.addAction(show_pathology_view)
        context.exec_(self.mapToGlobal(pos))

    def show_sector_view(self):
        sector_index = self.list.currentRow() + 1

        sector_model = SingleSectorDataModel(self.model, sector_index)
        sector_model.make()

        dialog = SingleSectorWindow(self.main, sector_model)
        dialog.show()

    def show_pathology_view(self):
        if self.model.pathology is None:
            return

        pathology = self.list.currentItem().text()
        image, notes = self.model.pathology.get(pathology, (None, None))
        dialog = ShowPathologyWindow(image, notes, self.main)
        dialog.show()


class BaseHeatmapWidget(QWidget):

    def __init__(self, main, new_canvas=Canvas, *args, **kwargs):
        super(BaseHeatmapWidget, self).__init__(*args, **kwargs)
        self.model = None

        self.main = main

        layout = QHBoxLayout(self)

        self.canvas = new_canvas()
        layout.addWidget(self.canvas, stretch=1)

        self.commands_pane = QVBoxLayout(self)
        layout.addLayout(self.commands_pane)

        self.profiles = ProfilesActions(self)
        self.commands_pane.addWidget(self.profiles, stretch=0)

        self.heatmap_legend = HeatmapLegend(self)
        self.commands_pane.addWidget(self.heatmap_legend)

        self.sectors_legend = SectorsLegend(self)
        self.commands_pane.addWidget(self.sectors_legend)

        self.commands_pane.addStretch(1)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.connect_profile_actions()

    def connect_profile_actions(self):
        self.canvas.signals.profile_selected.connect(
            self.profiles.on_profile_selected)
        self.canvas.signals.profile_selected.connect(
            self.profiles.on_profile_selected)

    def set_model(self, model):
        self.model = model
        self.canvas.set_model(model)
        self.profiles.set_model(model)
        self.heatmap_legend.set_model(model)
        self.sectors_legend.set_model(model)

    def update(self):
        if self.model is not None:
            self.canvas.redraw()
        super(BaseHeatmapWidget, self).update()


class BaseDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(BaseDialog, self).__init__(*args, **kwargs)
        self.signals = CloseSignals()

    def closeEvent(self, event):
        print("closing window...")
        self.signals.closing.emit()


class HeatmapWindow(BaseDialog):

    def __init__(self, main, model, new_canvas=Canvas,  *args, **kwargs):
        super(HeatmapWindow, self).__init__(main, *args, **kwargs)
        self.main = main
        layout = QVBoxLayout(self)

        self.base = BaseHeatmapWidget(
            self, new_canvas=new_canvas, *args, **kwargs)
        self.toolbar = self.base.toolbar
        layout.addWidget(self.toolbar)
        layout.addWidget(self.base)

        self.base.set_model(model)
        self.base.update()


class GuideWindowSignals(CloseSignals):
    selected_tracks_change = pyqtSignal(object)


class GuideWindow(BaseDialog):

    def __init__(self, main, model, *args, **kwargs):
        super(GuideWindow, self).__init__(main, *args, **kwargs)
        assert model.data.guide_df is not None
        self.width = 1000
        self.height = 500
        self.selected_tracks = set(model.selected_tracks)
        self.main = main
        layout = QVBoxLayout(self)
        self.guide_df = model.data.guide_df
        self.build_model()

        self.selected_tracks = set([
            s for s in self.selected_tracks if s in self.model_df.name.values
        ])

        self.signals = GuideWindowSignals()

        self.table = QTableWidget()
        self.table.setRowCount(len(self.guide_df.columns))
        self.table.setColumnCount(5)

        for index, row in self.model_df.iterrows():

            self.table.setItem(index, 0, QTableWidgetItem(str(index)))
            self.table.setItem(index, 1, QTableWidgetItem(row['name']))
            self.table.setItem(index, 2, QTableWidgetItem(str(row['dtype'])))
            self.table.setItem(
                index, 3, QTableWidgetItem(str(row['rank'])))
            checkbox = QCheckBox()
            if row['name'] in self.selected_tracks:
                checkbox.setChecked(True)
            checkbox.stateChanged.connect(
                partial(self.checkbox_clicked, row['name']))
            self.table.setCellWidget(
                index, 4, checkbox
            )

        self.table.move(0, 0)
        self.table.setHorizontalHeaderLabels([
            "No.", "Name", "Type", "Unique Values", "Selected"])

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        button_box = QHBoxLayout()
        apply_button = QPushButton("Apply")
        cancel_button = QPushButton("Cancel")

        apply_button.clicked.connect(
            self.on_apply_action)
        cancel_button.clicked.connect(
            self.on_cancel_action)

        button_box.addWidget(cancel_button)
        button_box.addWidget(apply_button)
        layout.addLayout(button_box)

    def on_apply_action(self):
        print("on_apply_action!!!", self.selected_tracks)
        self.signals.selected_tracks_change.emit(self.selected_tracks)
        self.close()

    def on_cancel_action(self):
        self.close()

    def build_model(self):
        dtypes = self.guide_df.dtypes
        data = defaultdict(list)
        for index, (name, dtype) in enumerate(dtypes.iteritems()):
            rank = len(self.guide_df[name].unique())
            data['index'].append(index)
            data['name'].append(name)
            data['dtype'].append(dtype)
            data['rank'].append(rank)

        self.model_df = pd.DataFrame(
            data, columns=['index', 'name', 'dtype', 'rank']
        )

    def checkbox_clicked(self, name, state):
        if state == Qt.Checked:
            self.selected_tracks.add(name)
        else:
            self.selected_tracks.remove(name)
        print(self.selected_tracks)


class SingleSectorWindow(BaseDialog):
    def __init__(self, main, sector_model, *args, **kwargs):
        super(SingleSectorWindow, self).__init__(main, *args, **kwargs)
        self.main = main
        layout = QVBoxLayout(self)

        self.base = BaseHeatmapWidget(self, *args, **kwargs)
        self.toolbar = self.base.toolbar
        layout.addWidget(self.toolbar)
        layout.addWidget(self.base)

        self.base.set_model(sector_model)

        self.base.update()

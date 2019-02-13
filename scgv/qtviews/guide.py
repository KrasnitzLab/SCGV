import pandas as pd
from collections import defaultdict
from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, \
    QPushButton, QTableWidget, QTableWidgetItem, QCheckBox

from scgv.qtviews.base import BaseDialog, CloseSignals


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

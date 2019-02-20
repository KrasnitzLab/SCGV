# import traceback
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QAction, \
    QComboBox, QPushButton, QFrame, QLabel

from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar

from scgv.qtviews.canvas import Canvas, SectorsCanvas
from scgv.qtviews.base import BaseDialog

from scgv.qtviews.profiles import ProfilesActions
from scgv.qtviews.legend import HeatmapLegend, LegendWidget


from scgv.models.sector_model import SingleSectorDataModel, \
    SingleTrackDataModel, SectorsDataModel, TrackDataModel

from scgv.qtviews.pathology_window import ShowPathologyWindow

from scgv.views.track import TrackViewer


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

        self.tracks_legend = TracksLegend(self)
        self.commands_pane.addWidget(self.tracks_legend)

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
        # self.tracks_legend.set_model(model)

    def update(self):
        if self.model is not None:
            self.canvas.redraw()
        self.tracks_legend.set_model(self.model)

        super(BaseHeatmapWidget, self).update()


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


class TrackLegendBase(QFrame):
    def __init__(self, main, title, *args, **kwargs):
        super(TrackLegendBase, self).__init__(main, *args, **kwargs)
        self.main = main

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.layout = QVBoxLayout(self)

        label = QLabel(self)
        label.setText(title)
        self.layout.addWidget(label)

        self.legend = LegendWidget(main, *args, **kwargs)
        self.layout.addWidget(self.legend)

        self.model = None
        self.mapping = None
        self.track = None

    def show(self):
        assert self.model is not None

        if self.mapping is None or self.track is None:
            return

        self.cmap = TrackViewer.select_colormap(self.mapping)
        vmin = min(self.mapping.values())

        self.legend.clear()
        for key, value in self.mapping.items():
            color = self.cmap.colors[int(value-vmin)]
            self.legend.add_entry(
                text=str(key),
                color=color)

    def set_context_menu_actions(self, context_menu_actions):
        self.legend.set_context_menu_actions(context_menu_actions)


class SectorsLegend(TrackLegendBase):

    def __init__(self, main, *args, **kwargs):
        super(SectorsLegend, self).__init__(main, "Sector:", *args, **kwargs)

        self.order_by_sector_button = \
            QPushButton("Order by Sector View", self)
        self.order_by_sector_button.pressed.connect(
            self.on_order_by_sector_action)
        self.layout.addWidget(self.order_by_sector_button)

    def set_model(self, model):
        self.legend.clear()

        self.legend.set_model(model)
        self.model = model
        if self.mapping is None or self.track is None:
            self.track, self.mapping = \
                self.model.make_sectors_legend()

        show_sector_view = QAction("Show sector view", self)
        show_sector_view.triggered.connect(self.show_sector_view)
        if self.model.pathology:
            show_pathology_view = QAction("Show sector pathology", self)
            show_pathology_view.triggered.connect(self.show_pathology_view)
            self.set_context_menu_actions([
                show_sector_view,
                show_pathology_view,
            ])
        else:
            self.set_context_menu_actions([
                show_sector_view,
            ])

        self.show()

    def show_sector_view(self):
        current_row = self.legend.list.currentRow()
        if current_row < 0:
            return

        sector_index = current_row + 1

        sector_model = SingleSectorDataModel(self.model, sector_index)
        sector_model.make()

        dialog = SingleSectorWindow(self.main, sector_model)
        dialog.show()

    def show_pathology_view(self):
        if self.model.pathology is None:
            return

        pathology = self.legend.list.currentItem().text()
        image, notes = self.model.pathology.get(pathology, (None, None))
        dialog = ShowPathologyWindow(image, notes, self.main)
        dialog.show()

    def on_order_by_sector_action(self, *args, **kwargs):
        if self.model is None:
            return

        self.order_by_sector_button.setEnabled(False)

        sectors_model = SectorsDataModel(self.model)
        sectors_model.make()

        dialog = HeatmapWindow(
            self.main, sectors_model, new_canvas=SectorsCanvas)
        dialog.signals.closing.connect(self.on_order_by_sector_closing)
        dialog.show()

    def on_order_by_sector_closing(self):
        self.order_by_sector_button.setEnabled(True)


class TracksLegend(TrackLegendBase):

    def __init__(self, main, *args, **kwargs):
        super(TracksLegend, self).__init__(main, "Tracks:", *args, **kwargs)

        self.combo = QComboBox(main)
        self.layout.insertWidget(1, self.combo)

        self.combo.currentIndexChanged.connect(self.current_track_changed)

        self.order_by_track_button = \
            QPushButton("Order by Track View", self)
        self.order_by_track_button.pressed.connect(
            self.on_order_by_track)
        self.layout.addWidget(self.order_by_track_button)

        self.tracks = None
        self.selected_track = None

    def set_model(self, model):
        self.legend.clear()
        self.combo.clear()

        self.legend.set_model(model)
        self.model = model
        self.tracks = self.model.tracks
        self.selected_track = None
        if self.tracks:
            self.selected_track = self.tracks[0]
            _, _, self.track, self.mapping = self.selected_track

        for index, track_name, track, mapping in self.tracks:
            self.combo.addItem(track_name)

        show_track_view = QAction("Show track view", self)
        show_track_view.triggered.connect(self.show_track_view)
        self.set_context_menu_actions([
            show_track_view,
        ])

        self.show()

    def current_track_changed(self, index):
        if index == -1:
            return

        self.selected_track = self.tracks[index]
        _, _, self.track, self.mapping = self.selected_track
        self.show()

    def show_track_view(self):
        current_row = self.legend.list.currentRow()
        if current_row < 0:
            return

        track_value_index = current_row

        track_index, _, _, mapping = self.selected_track
        track_value = list(mapping.values())[track_value_index]

        track_model = SingleTrackDataModel(
            self.model, track_index, track_value)
        track_model.make()

        dialog = SingleSectorWindow(self.main, track_model)
        dialog.show()

    def on_order_by_track(self, *args, **kwargs):
        if self.model is None:
            return

        self.order_by_track_button.setEnabled(False)
        track_index, _, _, _ = self.selected_track
        track_model = TrackDataModel(self.model, track_index)
        track_model.make()

        dialog = HeatmapWindow(
            self.main, track_model, new_canvas=SectorsCanvas)
        dialog.signals.closing.connect(self.on_order_by_track_closing)
        dialog.show()

    def on_order_by_track_closing(self):
        self.order_by_track_button.setEnabled(True)

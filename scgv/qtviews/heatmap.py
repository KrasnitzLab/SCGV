import numpy as np

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QAction, QMenu

from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar

from scgv.qtviews.canvas import Canvas
from scgv.qtviews.base import BaseDialog

from scgv.qtviews.profiles import ProfilesActions
from scgv.qtviews.legend import HeatmapLegend, LegendWidget


from scgv.models.sector_model import SingleSectorDataModel

from scgv.qtviews.pathology_window import ShowPathologyWindow

from scgv.utils.color_map import ColorMap
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
        self.tracks_legend.set_model(model)

    def update(self):
        if self.model is not None:
            self.canvas.redraw()
        self.tracks_legend.update(self.model)

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


class TracksLegend(LegendWidget):

    def __init__(self, main, *args, **kwargs):
        super(TracksLegend, self).__init__(main, *args, **kwargs)
        self.tracks = None
        self.selected_track = None

    def update(self, model):
        self.model = model
        self.tracks = None
        self.selected_track = None

        self.clear()
        self.show()

    def show(self):
        assert self.model is not None

        if self.tracks is None:
            self.tracks = self.model.tracks
        if not self.tracks:
            print("no tracks!!!!")
            return
        if self.selected_track is None:
            self.selected_track = self.tracks[0]

        index, track_name, track, mapping = self.selected_track
        self.cmap = TrackViewer.select_colormap(mapping)
        print("TracksLegend:", index, track_name, mapping)
        print(dir(self.cmap))
        print(self.cmap.colors)
        vmin = np.min(track)

        for key, value in mapping.items():
            color = self.cmap.colors[int(value-vmin)]
            print(color, type(color))

            self.add_entry(
                text=str(key),
                color=color)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # for (index, (sector, pathology)) in enumerate(self.sectors):
        #     color = self.cmap.colors(index)
        #     self.add_entry(
        #         text=pathology,
        #         color=color)

    def on_context_menu(self, pos, *args, **kwargs):
        show_track_view = QAction("Show track view", self)
        show_track_view.triggered.connect(self.show_track_view)

        context = QMenu(self)
        context.addAction(show_track_view)
        context.exec_(self.mapToGlobal(pos))

    def show_track_view(self):
        print("show_track_view")
        # sector_index = self.list.currentRow() + 1

        # sector_model = SingleSectorDataModel(self.model, sector_index)
        # sector_model.make()

        # dialog = SingleSectorWindow(self.main, sector_model)
        # dialog.show()

'''
Created on Feb 21, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport


from tkutils.open_ui import OpenUi
from tkutils.pinmat_ui import PinmatUi
from tkutils.sectors_ui import SectorsUi

from views.dendrogram import DendrogramViewer
from views.clone import CloneViewer
from views.heatmap import HeatmapViewer
from views.sector import SectorViewer
from views.gate import GateViewer
from views.multiplier import MultiplierViewer
from views.error import ErrorViewer
from controllers.controller import PinmatController, SectorsController
from cnviewer.pinmat_window import PinmatWindow
from cnviewer.base_window import BaseHeatmapWindow

import matplotlib.pyplot as plt
from models.sector_model import SectorDataModel
from cnviewer.sectors_window import SectorsWindow


class MainWindow(BaseHeatmapWindow):

    def __init__(self, master, controller):
        super(MainWindow, self).__init__(master, controller)
        self.controller.register_on_model_callback(self.on_model_callback)

    def build_ui(self):
        self.build_base_ui()

        pinmat = PinmatUi(self.main.button_ext, self.controller)
        pinmat.build_ui()
        pinmat.register_on_pinmat(self.build_pinmat)

        sectors = SectorsUi(self.main.button_ext, self.controller)
        sectors.build_ui()
        sectors.register_on_sectors_reorder(self.build_sectors_reorder)

        open_buttons = OpenUi(self.main.button_ext, self.controller)
        open_buttons.build_ui()

    def on_model_callback(self, model):
        self.model = model
        self.draw_canvas()

    def draw_canvas(self):
        ax_dendro = self.fig.add_axes([0.1, 0.775, 0.8, 0.175], frame_on=True)
        dendro_viewer = DendrogramViewer(self.model)
        dendro_viewer.draw_dendrogram(ax_dendro)

        ax_clone = self.fig.add_axes(
            [0.1, 0.7625, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer = CloneViewer(self.model)
        clone_viewer.draw_clone(ax_clone)
        ax_subclone = self.fig.add_axes(
            [0.1, 0.75, 0.8, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer.draw_subclone(ax_subclone)

        ax_heat = self.fig.add_axes(
            [0.1, 0.20, 0.8, 0.55], frame_on=True, sharex=ax_dendro)

        heatmap_viewer = HeatmapViewer(self.model)
        heatmap_viewer.draw_heatmap(ax_heat)
        # heatmap_viewer.draw_legend()

        ax_sector = self.fig.add_axes(
            [0.1, 0.175, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        # draw sector bar
        sector_viewer = SectorViewer(self.model)
        sector_viewer.draw_sector(ax_sector)

        ax_gate = self.fig.add_axes(
            [0.1, 0.150, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        gate_viewer = GateViewer(self.model)
        gate_viewer.draw_ploidy(ax_gate)

        ax_multiplier = self.fig.add_axes(
            [0.1, 0.125, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        multiplier_viewer = MultiplierViewer(self.model)
        multiplier_viewer.draw_multiplier(ax_multiplier)

        ax_error = self.fig.add_axes(
            [0.1, 0.10, 0.8, 0.025], frame_on=True, sharex=ax_dendro)
        error_viewer = ErrorViewer(self.model)
        error_viewer.draw_error(ax_error)
        error_viewer.draw_xlabels(ax_error)

        self.ax_label = ax_error

        plt.setp(ax_dendro.get_xticklabels(), visible=False)
        plt.setp(ax_clone.get_xticklabels(), visible=False)
        plt.setp(ax_clone.get_xticklines(), visible=False)
        plt.setp(ax_subclone.get_xticklabels(), visible=False)
        plt.setp(ax_subclone.get_xticklines(), visible=False)
        plt.setp(ax_heat.get_xticklabels(), visible=False)
        plt.setp(ax_sector.get_xticklabels(), visible=False)
        plt.setp(ax_gate.get_xticklabels(), visible=False)
        plt.setp(ax_multiplier.get_xticklabels(), visible=False)

        self.controller.event_loop_connect(self.fig)
        self.main.refresh()

    def build_pinmat(self, pinmat_button):
        pinmat_button.diable_ui()

        root = tk.Toplevel()
        controller = PinmatController(self.model)
        pinmat_window = PinmatWindow(root, controller)
        pinmat_window.build_ui()

        def on_close():
            pinmat_button.enable_ui()
        pinmat_window.register_on_closing_callback(on_close)

        pinmat_window.draw_canvas()
        root.mainloop()

    def build_sectors_reorder(self, sectors_button):
        sectors_button.disable_ui()

        root = tk.Toplevel()
        sectors_model = SectorDataModel(self.model)
        sectors_model.make()

        controller = SectorsController(sectors_model)

        sectors_window = SectorsWindow(root, controller)
        sectors_window.build_ui()

        def on_close():
            sectors_button.enable_ui()
        sectors_window.register_on_closing_callback(on_close)

        sectors_window.draw_canvas()
        root.mainloop()

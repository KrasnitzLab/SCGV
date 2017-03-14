'''
Created on Feb 21, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport

from tkviews.canvas_ui import CanvasWindow
from tkviews.sectors_legend import SectorsLegend
from tkviews.heatmap_legend import HeatmapLegend
from controllers.controller import SingleSectorController

import numpy as np
from models.sector_model import SingleSectorDataModel

import matplotlib.pyplot as plt

from views.clone import CloneViewer
from views.heatmap import HeatmapViewer
from views.sector import SectorViewer
from views.gate import GateViewer
from views.multiplier import MultiplierViewer
from views.error import ErrorViewer
import traceback
from views.dendrogram import DendrogramViewer
from utils.observer import DataObserver, ProfilesObserver
from models.subject import DataSubject, ProfilesSubject
from commands.widget import DisableCommand, EnableCommand
from commands.executor import CommandExecutor
from commands.profiles import ShowProfilesCommand,\
    ClearProfilesCommand, AddProfilesCommand


class AddProfileDialog(simpledialog.Dialog):

    def body(self, master):
        self.result = None

        ttk.Label(master, text="Profiles:").grid(row=0)
        self.entry = tk.Text(
            master,
            height=2,
            width=20,
        )
        self.entry.grid(row=0, column=1)
        return self.entry  # initial focus

    def apply(self):
        result = self.entry.get('1.0', tk.END)
        self.result = result
        return self.result


class ProfilesUi(DataObserver, ProfilesObserver):

    def __init__(self, frame, subject, profiles_subject):
        DataObserver.__init__(self, subject)
        ProfilesObserver.__init__(self, profiles_subject)
        self.frame = frame

    def build_ui(self):
        frame = ttk.Frame(
            self.frame,
            borderwidth=5,
            # relief='sunken'
        )
        frame.grid(
            row=20, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        label = ttk.Label(frame, text="Profiles")
        label.grid(column=0, row=1)

        self.profile_ui = tk.Listbox(frame, width=7, height=5)
        self.profile_ui.grid(
            column=0, row=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        s = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=self.profile_ui.yview)
        s.grid(column=1, row=10, sticky=(tk.N, tk.S))
        self.profile_ui['yscrollcommand'] = s.set

        self.add_profile = ttk.Button(
            master=frame, text="Add Profile", command=self._add_profile_dialog)
        self.add_profile.grid(
            column=0, row=11, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.show_profiles = ttk.Button(
            master=frame, text="Show Profiles", command=self._show_profiles)
        self.show_profiles.grid(
            column=0, row=12, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.clear_profiles = ttk.Button(
            master=frame, text="Clear Profiles", command=self._clear_profiles)
        self.clear_profiles.grid(
            column=0, row=13, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        disable_command = DisableCommand(
            self.add_profile,
            self.show_profiles,
            self.clear_profiles)
        CommandExecutor.execute(disable_command)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def update(self):
        self.model = self.get_model()
        if self.model is None:
            return
        enable_command = EnableCommand(
            self.add_profile,
            self.show_profiles,
            self.clear_profiles)
        CommandExecutor.execute(enable_command)

    def update_profiles(self):
        if self.get_profiles().get_available_profiles():
            self._add_profile_samples(
                self.get_profiles().get_available_profiles())
        elif self.get_profiles().get_removed_profiles():
            self.profile_ui.delete(0, 'end')

    def _add_profile_samples(self, samples):
        for profile in samples:
            profiles = self.profile_ui.get(0, 'end')
            if profile in profiles:
                continue
            self.profile_ui.insert("end", profile)
        profiles = self.profile_ui.get(0, 'end')

    def _show_profiles(self):
        print("show profiles called...")
        samples = self.profile_ui.get(0, 'end')
        if not samples:
            return

        CommandExecutor.execute(
            ShowProfilesCommand(self.model, self.profiles_subject),
        )

    def _clear_profiles(self):
        print("clear profiles called...")
        CommandExecutor.execute(
            ClearProfilesCommand(self.profiles_subject)
        )

    def _add_profile_dialog(self):
        print("add profile dialog added...")
        add_dialog = AddProfileDialog(self.master.master)
        # self.master.wait_window(add_dialog.top)
        profiles = add_dialog.result
        print("add profile result is: ", profiles)
        if profiles is None:
            return
        profiles = profiles.replace(',', ' ')
        profiles = [p.strip() for p in profiles.split()]
        profiles = [
            p for p in profiles
            if p in self.model.column_labels
        ]
        CommandExecutor.execute(
            AddProfilesCommand(self.profiles_subject, profiles)
        )


class BaseHeatmapWindow(DataObserver, ProfilesObserver):

    def __init__(self, master, controller, data_subject, profiles_subject):
        DataObserver.__init__(self, data_subject)
        ProfilesObserver.__init__(self, profiles_subject)

        self.master = master
        self.controller = controller
        self.ax_label = None

    def update(self):
        self.model = self.get_model()
        if self.model is not None:
            self.draw_canvas()

    def update_profiles(self):
        if self.get_profiles().get_available_profiles():
            self.highlight_profiles_labels(
                self.get_profiles().get_available_profiles())
        elif self.get_profiles().get_removed_profiles():
            self.unhighlight_profile_labels(
                self.get_profiles().get_removed_profiles())

    def refresh(self):
        self.main.refresh()

    def register_on_closing_callback(self, cb):
        self.main.register_on_closing_callback(cb)

    def draw_canvas(self):
        assert self.model is not None

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

        self.fig.canvas.mpl_connect('button_press_event', self.event_handler)
        self.fig.canvas.mpl_connect('key_press_event', self.event_handler)

        self.main.refresh()

    def event_handler(self, event):
        if event.name == 'button_press_event' and event.button == 3:
            sample = self.locate_sample_click(event)
            if not sample:
                return
            CommandExecutor.execute(
                AddProfilesCommand(self.profiles_subject, [sample])
            )

    def locate_sample_click(self, event):
        if event.xdata is None:
            return None
        xloc = int(event.xdata / self.model.interval_length)
        sample_name = self.model.column_labels[xloc]
        print("xloc: {}; sample name: {}".format(xloc, sample_name))
        return sample_name

    def build_ui(self):
        self.build_base_ui()

    def build_base_ui(self):
        self.main = CanvasWindow(self.master, self.controller)
        self.fig = self.main.fig

        profiles = ProfilesUi(
            self.main.button_ext, self.subject, self.profiles_subject)
        profiles.build_ui()

        sectors_legend = SectorsLegend(
            self.main.legend_ext, self.controller, self.subject)
        sectors_legend.build_ui(row=10)
        sectors_legend.register_show_single_sector_callback(
            self.build_single_sector_window)

        heatmap_legend = HeatmapLegend(
            self.main.legend_ext, self.controller, self.subject)
        heatmap_legend.build_ui(row=20)
        heatmap_legend.show_legend()

    def build_single_sector_window(self, model, sector_id):
        try:
            sector_model = SingleSectorDataModel(model, sector_id)
            sector_model.make()

            controller = SingleSectorController(sector_model)

            root = tk.Toplevel()
            data_subject = DataSubject()
            profiles_subject = ProfilesSubject()

            main = BaseHeatmapWindow(
                root, controller, data_subject, profiles_subject)
            main.build_ui()
            data_subject.set_model(sector_model)

            root.mainloop()
        except Exception:
            traceback.print_exc()

    def get_profile_indices(self, profiles):
        profile_indices = []
        for i, p in enumerate(self.model.column_labels):
            if p in profiles:
                profile_indices.append(i)

        profile_indices = np.array(profile_indices)
        return profile_indices

    def highlight_profiles_labels(self, profiles):
        if self.ax_label is None:
            return
        profile_indices = self.get_profile_indices(profiles)
        print("highlight profiles: {}".format(profile_indices))
        for index in profile_indices:
            self.ax_label.get_xticklabels()[index].set_color('red')
        self.refresh()

    def unhighlight_profile_labels(self, profiles):
        if self.ax_label is None:
            return
        profile_indices = self.get_profile_indices(profiles)
        print("unhighlight profiles: {}".format(profile_indices))
        for index in profile_indices:
            self.ax_label.get_xticklabels()[index].set_color('black')
        self.refresh()

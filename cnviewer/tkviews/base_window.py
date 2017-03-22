'''
Created on Feb 21, 2017

@author: lubo
'''
from tkviews.tkimport import *  # @UnusedWildImport

from tkviews.canvas_window import CanvasWindow
from controllers.controller import SingleSectorController

import numpy as np
from models.sector_model import SingleSectorDataModel

import matplotlib.pyplot as plt
import matplotlib.colors as col

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
from commands.executor import CommandExecutor
from commands.profiles import ShowProfilesCommand,\
    ClearProfilesCommand, AddProfilesCommand
from PIL import ImageTk, Image
from utils.color_map import ColorMap
from commands.command import Command


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

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        self.add_profile.config(state=tk.DISABLED)
        self.show_profiles.config(state=tk.DISABLED)
        self.clear_profiles.config(state=tk.DISABLED)

    def update(self, subject):
        if isinstance(subject, DataSubject):
            self.model = self.get_model()
            if self.model is None:
                return
            self.add_profile.config(state=tk.ACTIVE)
            self.show_profiles.config(state=tk.ACTIVE)
            self.clear_profiles.config(state=tk.ACTIVE)
        elif isinstance(subject, ProfilesSubject):
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
            self.frame
        )

    def _clear_profiles(self):
        print("clear profiles called...")
        CommandExecutor.execute(
            ClearProfilesCommand(self.profiles_subject),
            self.frame
        )

    def _add_profile_dialog(self):
        print("add profile dialog added...")
        add_dialog = AddProfileDialog(self.frame)
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
            AddProfilesCommand(self.profiles_subject, profiles),
            self.frame
        )


class ShowPathologyDialog(tk.Toplevel):

    def __init__(self, image, notes, master, title=None, **kwargs):
        self.image = image
        self.notes = notes
        tk.Toplevel.__init__(self, master, **kwargs)
        # super(ShowPathologyDialog, self).__init__(master, **kwargs)

        # self.transient(master)
        if title:
            self.title(title)

        self.master = master

        body = ttk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()

        # self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (master.winfo_rootx() + 50,
                                  master.winfo_rooty() + 50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def buttonbox(self):
        box = ttk.Frame(self)

        w = ttk.Button(
            box, text="OK", width=10, command=self.cancel, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.cancel)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.master.focus_set()
        self.destroy()

    def body(self, master):
        panel = None
        if self.image is not None:
            self.image = ImageTk.PhotoImage(self.image)
            panel = tk.Label(master, image=self.image)
            panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        text = tk.Text(master, width=80, height=20)
        scrollbar = tk.Scrollbar(master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        scrollbar.config(command=text.yview)
        text.config(yscrollcommand=scrollbar.set)

        if self.notes is not None:
            text.tag_configure('big', font=('Verdana', 15, 'bold'))
            text.insert(tk.END, self.notes[0], 'big')
            for line in self.notes[1:]:
                text.insert(tk.END, line)

        if panel is None:
            panel = text
        return panel


class LegendEntry(object):
    IMAGE_SIZE = 15

    def __init__(self, index, text, color):
        self.index = index
        self.text = text
        self.color = color
        self.image = None
        if color:
            tkcolor = self.tkcolor(color)
            image = Image.new(
                'RGBA',
                size=(self.IMAGE_SIZE, self.IMAGE_SIZE),
                color=tkcolor)
            self.image = ImageTk.PhotoImage(image=image)

    @staticmethod
    def tkcolor(color):
        c = col.to_rgba(color)
        if len(c) == 3:
            r, g, b = color
            a = 1
        elif len(c) == 4:
            r, g, b, a = color
        else:
            raise ValueError("strange color: {}".format(str(color)))
        return (int(255 * r), int(255 * g), int(255 * b), int(255 * a))

    def build_label(self, master):
        self.label = ttk.Label(
            master,
            text=self.text,
            image=self.image,
            compound=tk.LEFT,
            background='white',
        )
        self.label.pack(anchor=tk.W)

    def bind_dbl_left_click(self, callback):
        def click_callback(index):
            return lambda event: callback(index)
        self.label.bind('<Double-Button-1>', click_callback(self.index))

    def bind_dbl_right_click(self, callback):
        def click_callback(index):
            return lambda event: callback(index)
        self.label.bind('<Double-Button-3>', click_callback(self.index))

    def bind_right_click(self, callback):
        def click_callback(index):
            return lambda event: callback(index)
        self.label.bind('<Button-3>', click_callback(self.index))


class LegendBase(DataObserver):

    def __init__(self, master, title, controller, subject):
        super(LegendBase, self).__init__(subject)
        self.title = title
        self.master = master
        self.controller = controller

    def update(self, subject):
        assert isinstance(subject, DataSubject)
        self.model = self.get_model()

    def build_ui(self, row=20):
        self.entries = []
        frame = ttk.Frame(
            self.master,
            borderwidth=5,
            # relief='sunken',
        )
        frame.grid(row=row, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        label = ttk.Label(frame, text=self.title)
        label.grid(column=0, row=0, columnspan=2)

        scrollbar = ttk.Scrollbar(
            frame, orient=tk.VERTICAL)
        scrollbar.grid(column=1, row=1, sticky=(tk.N, tk.S))

        self.canvas = tk.Canvas(
            frame,
            yscrollcommand=scrollbar.set,
            height=100, width=100,
            background='white')
        self.canvas.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.config(command=self.canvas.yview)

        def configure_update(event):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.canvas.bind(
            '<Configure>',
            configure_update)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(20, weight=1)

        self.container = tk.Frame(self.canvas, background='white')
        self.canvas.create_window((0, 0), window=self.container, anchor='nw')

        configure_update(None)

    def append_entry(self, text, color=None):
        index = len(self.entries)
        entry = LegendEntry(index, text, color)
        entry.build_label(self.container)
        self.entries.append(entry)

    def configure_update(self, *args, **kwargs):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def bind_dbl_left_click(self, callback):
        for entry in self.entries:
            entry.bind_dbl_left_click(callback)

    def bind_dbl_right_click(self, callback):
        for entry in self.entries:
            entry.bind_dbl_right_click(callback)

    def bind_right_click(self, callback):
        for entry in self.entries:
            entry.bind_right_click(callback)


class HeatmapLegend(LegendBase):
    COPYNUM_LABELS = [
        "    0", "    1", "    2", "    3", "    4+"
    ]

    def __init__(self, master, controller, subject):
        super(HeatmapLegend, self).__init__(
            master,
            title="Heatmap Legend",
            controller=controller,
            subject=subject)

    def show_legend(self):
        cmap = ColorMap.make_diverging05()
        for index, label in enumerate(self.COPYNUM_LABELS):
            color = cmap.colors(index)
            self.append_entry(label, color)


class ShowSingleSectorCommand(Command):

    def __init__(self, model, sector_id):
        self.model = model
        self.sector_id = sector_id

    def execute(self):
        try:
            sector_model = SingleSectorDataModel(self.model, self.sector_id)
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


class SectorsLegend(LegendBase):

    def __init__(self, master, controller, subject):
        super(SectorsLegend, self).__init__(
            master, title="Sectors Legend",
            controller=controller,
            subject=subject)

    def update(self, subject):
        super(SectorsLegend, self).update(subject)
        if self.model is None:
            return
        self.sectors = self.model.make_sectors_legend()
        if self.sectors is None:
            return

        self.cmap = ColorMap.make_qualitative12()

        for (index, (sector, pathology)) in enumerate(self.sectors):
            color = self.cmap.colors(index)
            self.append_entry(
                text='{}: {}'.format(sector, pathology),
                color=color)

        self.bind_right_click(self.show_sector_pathology)
        self.bind_dbl_left_click(self.show_single_sector)
        self.master.after(500, self.configure_update, self)

    def show_sector_pathology(self, index):
        if self.sectors is None:
            return
        (_sector, pathology) = self.sectors[index]
        if self.model.pathology is None:
            print("model.pathology is None; stopping...")
            return
        image, notes = self.model.pathology.get(
            pathology, (None, None))
        if image is None and notes is None:
            return
        ShowPathologyDialog(image, notes, self.master)

    def show_single_sector(self, index):
        if self.sectors is None:
            return
        (sector, _) = self.sectors[index]
        CommandExecutor.execute(
            ShowSingleSectorCommand(self.model, sector),
            self.master)


class BaseHeatmapWindow(DataObserver, ProfilesObserver):

    def __init__(self, master, controller, data_subject, profiles_subject):
        DataObserver.__init__(self, data_subject)
        ProfilesObserver.__init__(self, profiles_subject)

        self.master = master
        self.controller = controller
        self.ax_label = None

    def update(self, subject):
        if isinstance(subject, DataSubject):
            self.model = self.get_model()
            if self.model is not None:
                self.draw_canvas()
        elif isinstance(subject, ProfilesSubject):
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

    W = 0.8875
    X = 0.075

    def draw_canvas(self):
        assert self.model is not None

        ax_dendro = self.fig.add_axes(
            [self.X, 0.775, self.W, 0.175], frame_on=True)
        dendro_viewer = DendrogramViewer(self.model)
        dendro_viewer.draw_dendrogram(ax_dendro)

        ax_clone = self.fig.add_axes(
            [self.X, 0.7625, self.W, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer = CloneViewer(self.model)
        clone_viewer.draw_clone(ax_clone)
        ax_subclone = self.fig.add_axes(
            [self.X, 0.75, self.W, 0.0125], frame_on=True, sharex=ax_dendro)
        clone_viewer.draw_subclone(ax_subclone)

        ax_heat = self.fig.add_axes(
            [self.X, 0.20, self.W, 0.55], frame_on=True, sharex=ax_dendro)

        heatmap_viewer = HeatmapViewer(self.model)
        heatmap_viewer.draw_heatmap(ax_heat)

        ax_sector = self.fig.add_axes(
            [self.X, 0.175, self.W, 0.025], frame_on=True, sharex=ax_dendro)
        # draw sector bar
        sector_viewer = SectorViewer(self.model)
        sector_viewer.draw_sector(ax_sector)

        ax_gate = self.fig.add_axes(
            [self.X, 0.150, self.W, 0.025], frame_on=True, sharex=ax_dendro)
        gate_viewer = GateViewer(self.model)
        gate_viewer.draw_ploidy(ax_gate)

        ax_multiplier = self.fig.add_axes(
            [self.X, 0.125, self.W, 0.025], frame_on=True, sharex=ax_dendro)
        multiplier_viewer = MultiplierViewer(self.model)
        multiplier_viewer.draw_multiplier(ax_multiplier)

        ax_error = self.fig.add_axes(
            [self.X, 0.10, self.W, 0.025], frame_on=True, sharex=ax_dendro)
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

        self.main.refresh()
        self.connect_event_loop()

    def connect_event_loop(self):
        self.fig.canvas.mpl_connect('button_press_event', self.event_handler)
        self.fig.canvas.mpl_connect('key_press_event', self.event_handler)

    def event_handler(self, event):
        if event.name == 'button_press_event' and event.button == 3:
            sample = self.locate_sample_click(event)
            if not sample:
                return
            CommandExecutor.execute(
                AddProfilesCommand(self.profiles_subject, [sample]),
                self.master
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

        heatmap_legend = HeatmapLegend(
            self.main.legend_ext, self.controller, self.subject)
        heatmap_legend.build_ui(row=20)
        heatmap_legend.show_legend()

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

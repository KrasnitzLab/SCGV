'''
Created on Jan 17, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport


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
        print(result)  # or something
        self.result = result
        return self.result


class ProfilesUi(object):

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

    def build_ui(self):
        frame = ttk.Frame(
            self.master,
            borderwidth=5,
            relief='sunken')
        frame.grid(
            row=20, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        label = ttk.Label(frame, text="Profiles")
        label.grid(column=0, row=1)

        self.profile_ui = tk.Listbox(frame, width=7, height=7)
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

        self.add_profile.config(state=tk.DISABLED)
        self.show_profiles.config(state=tk.DISABLED)
        self.clear_profiles.config(state=tk.DISABLED)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        self._connect_controller()

    def _connect_controller(self):
        if self.controller.model is None:
            self.controller.register_on_model_callback(
                self.enable_profile_buttons)
        else:
            self.enable_profile_buttons(self.controller.model)

        self.controller.register_sample_cb(
            self.on_add_samples_callback,
            None,
            None
        )

    def enable_profile_buttons(self, model):
        self.add_profile.config(state=tk.ACTIVE)
        self.show_profiles.config(state=tk.ACTIVE)
        self.clear_profiles.config(state=tk.ACTIVE)

    def on_add_samples_callback(self, samples):
        for sample in samples:
            profiles = self.profile_ui.get(0, 'end')
            if sample in profiles:
                continue
            self.profile_ui.insert("end", sample)

    def _add_profile_samples(self, samples):
        for sample in samples:
            profiles = self.profile_ui.get(0, 'end')
            if sample in profiles:
                continue
            self.profile_ui.insert("end", sample)
        profiles = self.profile_ui.get(0, 'end')
        self.controller.add_samples(profiles)
        # self.controller.highlight_profiles_labels(profiles)

    def _show_profiles(self):
        print("show profiles called...")
        samples = self.profile_ui.get(0, 'end')
        if not samples:
            return

        self._clear_profiles()
        self.controller.display_samples(samples)

    def _clear_profiles(self):
        print("clear profiles called...")
        profiles = self.profile_ui.get(0, 'end')
        self.profile_ui.delete(0, 'end')
        self.controller.clear_samples(profiles)
        # self.controller.unhighlight_profile_labels(profiles)

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
            if p in self.controller.model.column_labels
        ]
        self._add_profile_samples(profiles)

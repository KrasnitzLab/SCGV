'''
Created on Jan 17, 2017

@author: lubo
'''
import sys  # @UnusedImport
if sys.version_info[0] < 3:
    import Tkinter as tk  # @UnusedImport @UnresolvedImport
    import ttk  # @UnusedImport @UnresolvedImport
    from tkFileDialog import askopenfilename  # @UnusedImport @UnresolvedImport
    import tkMessageBox as messagebox  # @UnusedImport @UnresolvedImport
    import tkSimpleDialog as simpledialog  # @UnusedImport @UnresolvedImport
else:
    import tkinter as tk  # @Reimport @UnresolvedImport
    from tkinter import ttk  # @UnresolvedImport @UnusedImport @Reimport
    from tkinter.filedialog \
        import askopenfilename  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter.filedialog \
        import askdirectory  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter import messagebox  # @UnresolvedImport @Reimport @UnusedImport
    from tkinter import simpledialog  # @UnresolvedImport @Reimport @UnusedImport @IgnorePep8


class AddProfileDialog(simpledialog.Dialog):

    def body(self, master):
        self.result = None

        ttk.Label(master, text="Profile:").grid(row=0)
        self.entry = ttk.Entry(master)
        self.entry.grid(row=0, column=1)
        return self.entry  # initial focus

    def apply(self):
        result = self.entry.get()
        print(result)  # or something
        self.result = result
        return self.result


class ProfilesUi(object):

    def __init__(self, master, canvas):
        self.master = master
        self.controller = None
        self.canvas = canvas

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

    def _add_profile_sample(self, sample):
        profiles = self.profile_ui.get(0, 'end')
        if sample in profiles:
            return
        self.profile_ui.insert("end", sample)
        profiles = self.profile_ui.get(0, 'end')
        self.controller.highlight_profiles_labels(profiles)
        self.canvas.refresh()

    def connect_controller(self, controller):
        assert controller is not None
        self.controller = controller
        self.controller.register_sample_cb(self._add_profile_sample)

        self.add_profile.config(state=tk.ACTIVE)
        self.show_profiles.config(state=tk.ACTIVE)
        self.clear_profiles.config(state=tk.ACTIVE)

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
        self.controller.unhighlight_profile_labels(profiles)
        self.profile_ui.delete(0, 'end')
        self.canvas.refresh()

    def _add_profile_dialog(self):
        print("add profile dialog added...")
        add_dialog = AddProfileDialog(self.master.master)
        # self.master.wait_window(add_dialog.top)
        profile = add_dialog.result
        print("add profile result is: ", profile)
        if profile in self.controller.model.column_labels:
            self._add_profile_sample(profile)
        else:
            print("wrong sample name: ", profile)

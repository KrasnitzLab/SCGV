'''
Created on Jan 18, 2017

@author: lubo
'''
import sys  # @UnusedImport
from tkutils.canvas_ui import CanvasWindow
from views.controller import MainController
from tkutils.profiles_ui import ProfilesUi
if sys.version_info[0] < 3:
    import Tkinter as tk  # @UnusedImport @UnresolvedImport
    import ttk  # @UnusedImport @UnresolvedImport
    from tkFileDialog import askopenfilename  # @UnusedImport @UnresolvedImport
    import tkMessageBox as messagebox  # @UnusedImport @UnresolvedImport
else:
    import tkinter as tk  # @Reimport @UnresolvedImport
    from tkinter import ttk  # @UnresolvedImport @UnusedImport @Reimport
    from tkinter.filedialog \
        import askopenfilename  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter.filedialog \
        import askdirectory  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter import messagebox  # @UnresolvedImport @Reimport @UnusedImport


class PinmatUi(object):

    def __init__(self, master):
        self.master = master
        self.controller = None

    def build_ui(self):
        frame = ttk.Frame(
            self.master,
            borderwidth=5)
        frame.grid(
            row=20, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.show_pinmat = ttk.Button(
            master=frame, text="Show Pins", command=self._show_pinmat)
        self.show_pinmat.config(state=tk.DISABLED)

        self.show_pinmat.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def _show_pinmat(self):
        self.show_pinmat.config(state=tk.DISABLED)

        print("show pins called...")
        if self.controller is None:
            return
        assert self.controller is not None

        controller = MainController(self.controller.model)
        root = tk.Toplevel()
        main = CanvasWindow(root)

        profiles = ProfilesUi(main.button_ext)
        profiles.build_ui()
        main.register_on_controller_callback(profiles.connect_controller)

        controller.build_pinmat(main.fig)
        main.connect_controller(controller)

        root.mainloop()

    def connect_controller(self, controller):
        assert controller is not None
        self.controller = controller

        self.show_pinmat.config(state=tk.ACTIVE)

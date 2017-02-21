'''
Created on Jan 18, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport

from tkutils.canvas_ui import CanvasWindow
from controllers.controller import MainController
from tkutils.profiles_ui import ProfilesUi


class PinmatWindow(CanvasWindow):

    def __init__(self, root):
        super(PinmatWindow, self).__init__(root)
        profiles = ProfilesUi(self.button_ext, self)
        profiles.build_ui()
        self.register_on_controller_callback(profiles.connect_controller)


class PinmatUi(object):

    def __init__(self, master):
        self.master = master
        self.controller = None
        self.root = None

    def build_ui(self):
        frame = ttk.Frame(
            self.master,
            borderwidth=5)
        frame.grid(
            row=30, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

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
        self.root = tk.Toplevel()
        main = PinmatWindow(self.root)

        controller.build_pinmat(main.fig)
        main.connect_controller(controller)
        main.register_on_closing_callback(self.on_closing)

        self.root.mainloop()

    def on_closing(self):
        print("PinmatUi::on_closing called...")
        self.show_pinmat.config(state=tk.ACTIVE)

    def connect_controller(self, controller):
        assert controller is not None
        self.controller = controller

        self.show_pinmat.config(state=tk.ACTIVE)

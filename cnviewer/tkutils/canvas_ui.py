'''
Created on Jan 18, 2017

@author: lubo
'''
import matplotlib as mpl
from tkutils.sectors_legend import SectorsLegend
mpl.use('TkAgg')


from matplotlib.backends.backend_tkagg import * # @UnusedWildImport @IgnorePep8
from matplotlib.figure import Figure  # @IgnorePep8 @Reimport

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


class CanvasWindow(object):

    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.fig = Figure(figsize=(12, 8))

        self.content = tk.Frame(self.root)
        self.content.pack(side="top", fill="both", expand=True)

        self.canvas = FigureCanvasTkAgg(self.fig, self.content)
        self.canvas.show()

        toolbar_frame = ttk.Frame(
            self.content,
            # relief='sunken',
            borderwidth=5,
        )
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        self.toolbar.update()

        self.toolbar_ext = ttk.Frame(
            toolbar_frame,
            # relief='sunken',
            borderwidth=5,
            # width=150
        )
        self.button_ext = ttk.Frame(
            self.content, borderwidth=1,
            # width=150
        )

        self.toolbar.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvas.get_tk_widget().grid(
            column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        toolbar_frame.grid(
            column=0, row=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        toolbar_frame.columnconfigure(0, weight=0)
        toolbar_frame.columnconfigure(1, weight=1)

        self.toolbar_ext.grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.toolbar_ext.columnconfigure(0, weight=99)
        self.button_ext.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.content.columnconfigure(0, weight=99)
        self.content.rowconfigure(0, weight=0)
        self.content.columnconfigure(1, weight=0)
        self.content.rowconfigure(1, weight=99)

        self._build_button_ext()
        self._build_legend_ext()

        self.on_controller_callbacks = []
        self.on_closing_callbacks = []

    def register_on_controller_callback(self, cb):
        self.on_controller_callbacks.append(cb)

    def register_on_closing_callback(self, cb):
        self.on_closing_callbacks.append(cb)

    def connect_controller(self, controller):
        for cb in self.on_controller_callbacks:
            cb(controller)

        self.sectors_legend.register_controller(controller)
        self.canvas.draw()

    def refresh(self):
        self.canvas.draw()

    def _build_button_ext(self):
        frame = ttk.Frame(
            self.button_ext,
            # relief='sunken',
            borderwidth=5)
        frame.grid(
            row=50, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.quit_button = ttk.Button(
            master=frame,
            text='Close',
            command=self.on_closing)
        self.quit_button.grid(
            row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def _build_legend_ext(self):
        frame = ttk.Frame(
            self.button_ext,
            relief='sunken',
            borderwidth=5)
        frame.grid(row=100, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        self.sectors_legend = SectorsLegend(frame)
        self.sectors_legend.build_ui()

    def on_closing(self):
        print("CanvasWindow::on_closing called...")
        for cb in self.on_closing_callbacks:
            cb()

        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

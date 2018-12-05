from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog

from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from scgv.views.sample import SamplesViewer


class ShowProfilesWindow(QDialog):

    def __init__(self, model, profiles, parent, *args, **kwargs):
        super(ShowProfilesWindow, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("SCGV Show Profiles")

        self._main = QWidget(self)
        layout = QVBoxLayout(self)

        self.fig = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.fig)

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.model = model
        self.profiles = profiles

        self.draw_canvas()
        self.canvas.draw()

    def draw_canvas(self):
        samples_viewer = SamplesViewer(self.model)
        samples_viewer.draw_samples(self.fig, self.profiles)
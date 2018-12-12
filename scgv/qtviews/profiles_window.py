import webbrowser
import numpy as np

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog
from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import Qt


from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from scgv.views.sample import SamplesViewer


class Signals(QObject):
    position_selected = pyqtSignal(object)


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

        self.signals = Signals()
        self.cid = None

        self.cid = self.fig.canvas.mpl_connect(
            "button_press_event", self.onclick)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        self.browse_position = None

    def on_context_menu(self, pos, *args, **kwargs):
        open_browser = QAction("Open UCSC Genome Browser", self)
        open_browser.triggered.connect(self.on_open_genome_browser)

        context = QMenu(self)
        context.addAction(open_browser)
        context.exec_(self.mapToGlobal(pos))

    def on_open_genome_browser(self):
        genome = self.model.data.genome
        assert genome is not None

        if self.browse_position is None:
            print("UCSC Genome Broser position not found....")
            return

        chrom, pos = self.browse_position
        self.browse_position = None
        if 'hg' in genome:
            if chrom == 23:
                chrom = 'X'
            if chrom == 24:
                chrom = 'Y'
        if 'mm' in genome:
            if chrom == 20:
                chrom = 'X'
            if chrom == 21:
                chrom = 'Y'

        position = 'chr{}:{}'.format(chrom, pos)
        url = "http://genome.ucsc.edu/cgi-bin/hgTracks?db={}&position={}"\
            .format(genome, position)
        print('opening url: ', url)
        webbrowser.open(url, new=False, autoraise=True)

    def draw_canvas(self):
        samples_viewer = SamplesViewer(self.model)
        samples_viewer.draw_samples(self.fig, self.profiles)

    def translate_xcoord(self, xdata):
        index = np.abs(self.model.data.seg_df.abspos.values - xdata).argmin()
        chrom, chrompos = self.model.data.seg_df.iloc[index, [0, 1]]
        return (int(chrom), int(chrompos))

    def onclick(self, event):
        print(
            '%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            ('double' if event.dblclick else 'single', event.button,
             event.x, event.y, event.xdata, event.ydata))

        chrom, pos = self.translate_xcoord(event.xdata)
        print(chrom, pos)
        if event.name == 'button_press_event' and event.button == 3:
            self.browse_position = chrom, pos

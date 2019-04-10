import webbrowser
import numpy as np

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt5.QtWidgets import QAction, QMenu
# from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import Qt


from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from scgv.qtviews.base import BaseDialog
from scgv.views.sample import SamplesViewer


class ShowProfilesWindow(BaseDialog):

    def __init__(self, model, profiles, parent, *args, **kwargs):
        super(ShowProfilesWindow, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("SCGV Show Profiles")

        self._main = QWidget(self)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.fig = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.fig)

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.model = model
        self.profiles = profiles

        self.draw_canvas()
        self.canvas.draw()

        self.cid = None

        self.cid = self.fig.canvas.mpl_connect(
            "button_press_event", self.onclick)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        self.browse_position = None
        self.browse_position_start = None
        self.browse_position_region = False

    def on_context_menu(self, pos, *args, **kwargs):
        open_browser = QAction("Open in UCSC Genome Browser", self)
        open_browser.triggered.connect(self.on_open_genome_browser)

        if self.browse_position_region:
            open_browser_region = QAction(
                "Open Region in UCSC Genome Browser End", self)
            open_browser_region.triggered.connect(
                self.on_open_genome_browser_region_end)
        else:
            open_browser_region = QAction(
                "Open Region in UCSC Genome Browser Start", self)
            open_browser_region.triggered.connect(
                self.on_open_genome_browser_region_start)

        context = QMenu(self)
        context.addAction(open_browser_region)
        context.addAction(open_browser)
        context.exec_(self.mapToGlobal(pos))

    def on_open_genome_browser(self):
        genome = self.model.data.genome
        assert genome is not None

        if self.browse_position_start is None:
            print("UCSC Genome Broser position not found....")
            return

        chrom, pos = self.browse_position_start
        self.browse_position_start = None
        chrom = self.ucsc_chrom(chrom)

        position = 'chr{}:{}'.format(chrom, pos)
        url = "http://genome.ucsc.edu/cgi-bin/hgTracks?db={}&position={}"\
            .format(genome, position)
        print('opening url: ', url)
        webbrowser.open(url, new=False, autoraise=True)

    def on_open_genome_browser_region_start(self):
        genome = self.model.data.genome
        assert genome is not None

        if self.browse_position is None:
            print("UCSC Genome Broser position not found....")
            return

        chrom, pos = self.browse_position
        self.browse_position_region = True
        self.browse_position_start = self.browse_position
        self.browse_position = None
        QApplication.setOverrideCursor(Qt.SplitHCursor)

    def ucsc_chrom(self, chrom):
        genome = self.model.data.genome
        assert genome is not None

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
        return chrom

    def on_open_genome_browser_region_end(self):
        genome = self.model.data.genome
        assert genome is not None

        if self.browse_position is None or self.browse_position_start is None:
            self.browse_position = None
            self.browse_position_start = None
            QApplication.setOverrideCursor(Qt.ArrowCursor)

            print("UCSC Genome Broser position not found....")
            return

        QApplication.setOverrideCursor(Qt.ArrowCursor)

        chrom_end, pos_end = self.browse_position
        chrom_start, pos_start = self.browse_position_start
        chrom_start = self.ucsc_chrom(chrom_start)
        chrom_end = self.ucsc_chrom(chrom_end)

        self.browse_position_region = False
        self.browse_position = None
        self.browse_position_start = None

        if chrom_start != chrom_end:
            print("region in different chromosomes")
            return
        chrom = chrom_start
        start = min(pos_start, pos_end)
        end = max(pos_start, pos_end)

        position = 'chr{}:{}-{}'.format(chrom, start, end)
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

        if event.name == 'button_press_event':
            if event.button == 3:
                self.browse_position = chrom, pos

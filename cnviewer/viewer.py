'''
Created on Dec 2, 2016

@author: lubo
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from utils.loader import load_df
from scipy.cluster.hierarchy import linkage, dendrogram
from utils.color_map import ColorMap


class ViewerBase(object):
    CHROM_LABELS = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
        "14", "15", "16", "17", "18", "19", "20", "21", "22", "X", "Y"
    ]

    COPYNUM_LABELS = ["0", "1", "2", "3", "4", "5+"]

    @staticmethod
    def calc_chrom_lines_pos(df):
        assert df is not None
        chrom_pos = df.chrom.values
        chrom_shift = np.roll(chrom_pos, -1)
        chrom_boundaries = chrom_pos != chrom_shift
        chrom_boundaries[0] = True
        chrom_lines = np.where(chrom_boundaries)
        return chrom_lines[0]

    @staticmethod
    def calc_chrom_labels_pos(chrom_lines):
        yt = (np.roll(chrom_lines, -1) - chrom_lines) / 2.0
        return (chrom_lines + yt)[:-1]

    @staticmethod
    def debug_event(event):
        # print(event)
        if event.name == 'button_press_event':
            print("MOUSE: name={}; xy=({},{}); xydata=({},{}); "
                  "button={}; dblclick={}".format(
                      event.name,
                      event.x, event.y,
                      event.xdata, event.ydata,
                      event.button, event.dblclick
                  ))
        elif event.name == 'key_press_event':
            print("KEY: name={}; xy=({},{}); xydata=({},{}); "
                  "key={}".format(
                      event.name,
                      event.x, event.y,
                      event.xdata, event.ydata,
                      event.key
                  ))
        else:
            print("???: {}".format(event.name))


class HeatmapViewer(ViewerBase):

    def __init__(self, seg_df):
        super(HeatmapViewer, self).__init__()
        self.seg_df = seg_df
        self.seg_data = seg_df.ix[:, 3:].values
        self.bins, self.samples = self.seg_data.shape
        self.interval_length = None
        self.Z = None
        self.lmat = None
        self.cmap = ColorMap.make_cmap01()
        self.sample_list = []

    def make_column_labels(self):
        assert self.direct_lookup
        assert self.seg_df is not None

        self.column_labels = \
            np.array(self.seg_df.columns[3:])[self.direct_lookup]
        return self.column_labels

    def make_dendrogram(self, ax, no_plot=False):
        if self.Z is not None:
            return
        self.Z = dendrogram(self.lmat, ax=ax, no_plot=no_plot)
        min_x = np.min(self.Z['icoord'])
        max_x = np.max(self.Z['icoord'])
        self.interval_length = (max_x - min_x) / (self.samples - 1)
        self.direct_lookup = self.Z['leaves']
        self.label_midpoints = (
            np.arange(self.samples) + 0.5) * self.interval_length
        self.make_column_labels()

    def make_linkage(self):
        if self.lmat is not None:
            return
        self.lmat = linkage(self.seg_data.transpose(), method='ward')

    def draw_dendogram(self, ax):
        assert self.seg_data is not None
        self.make_linkage()
        self.make_dendrogram(ax)

        ax.set_xticks(self.label_midpoints)
        ax.set_xticklabels([''] * len(self.column_labels))

    def make_legend(self):
        copynum_patches = []
        for color in self.cmap.colors.colors:
            copynum_patches.append(
                patches.Rectangle((0, 0), 0, 0, facecolor=color))
        plt.figlegend(copynum_patches, self.COPYNUM_LABELS, "upper right",
                      title="Copy #", prop={'size': 10})

    def draw_heatmap(self, ax):
        heat_extent = (0, self.samples * self.interval_length,
                       self.bins, 0)
        data = np.round(self.seg_data)

        ax.imshow(data[:, self.direct_lookup],
                  aspect='auto',
                  interpolation='nearest',
                  cmap=self.cmap.colors,
                  norm=self.cmap.norm,
                  extent=heat_extent)
        ax.set_xticks(self.label_midpoints)
        ax.set_xticklabels(self.column_labels,
                           rotation='vertical',
                           fontsize=10)
        chrom_lines = self.calc_chrom_lines_pos(self.seg_df)
        for chrom_line in chrom_lines:
            plt.axhline(y=chrom_line, color="#000000", linewidth=1)
        chrom_labelspos = self.calc_chrom_label_spos(chrom_lines)
        ax.set_yticks(chrom_labelspos)
        ax.set_yticklabels(self.CHROM_LABELS, fontsize=9)

    def locate_sample_click(self, event):
        if event.xdata is None:
            return None
        xloc = int(event.xdata / self.interval_length)
        sample_name = self.column_labels[xloc]
        print("xloc: {}; sample name: {}".format(xloc, sample_name))
        return sample_name

    def event_handler(self, event):
        print("event tester called...")
        self.debug_event(event)
        if event.name == 'button_press_event':
            sample = self.locate_sample_click(event)
            self.add_sample(sample)
        elif event.name == 'key_press_event' and event.key == 'd':
            print(self.sample_list)

            self.display_samples()
            self.sample_list = []

    def event_loop_connect(self, fig):
        fig.canvas.mpl_connect('button_press_event', self.event_handler)
        fig.canvas.mpl_connect('key_press_event', self.event_handler)

    def add_sample(self, sample):
        if sample is None:
            return
        if sample in self.sample_list:
            return
        self.sample_list.append(sample)

    def display_samples(self):
        pass


def main_heatmap():
    seg_filename = 'tests/data/sample.YL2671P11.5k.seg.quantal.primary.txt'
    seg_df = load_df(seg_filename)

    assert seg_df is not None

    viewer = HeatmapViewer(seg_df)

    fig = plt.figure(0, figsize=(12, 8))
    fig.suptitle(seg_filename, fontsize=10)

    ax_dendro = fig.add_axes([0.1, 0.75, 0.8, 0.2], frame_on=True)
    # draw_dendrogram(df, ax_dendro)
    viewer.draw_dendogram(ax_dendro)

    ax_heat = fig.add_axes(
        [0.1, 0.10, 0.8, 0.65], frame_on=True, sharex=ax_dendro)
    viewer.draw_heatmap(ax_heat)
    viewer.make_legend()

    viewer.event_loop_connect(fig)

    plt.show()


class SampleViewer(ViewerBase):

    def __init__(self, seg_df, ratio_df, sample_list):
        self.seg_df = seg_df
        self.ratio_df = ratio_df
        self.seg_data = seg_df.ix[:, 3:].values
        self.ratio_data = ratio_df.ix[:, 3:].values
        self.sample_list = sample_list

    def calc_chrom_lines(self):
        chrom_lines = self.calc_chrom_lines_pos(self.seg_df)
        return self.seg_df['abspos'][chrom_lines]

    def calc_ploidy(self, sample):
        return np.mean(self.seg_data[sample])

    def upto_chrom_x(self, df):
        chrom_x_index = np.where(self.seg_df['chrom'] == 23)
        print(chrom_x_index)
        return chrom_x_index

    def calc_error(self):
        pass

    def calc_shredded(self):
        pass

    def draw_samples(self):
        fig = plt.figure(figsize=(12, 8))

        chrom_lines = self.calc_chrom_lines()

        for num, sample in enumerate(self.sample_list):
            ax = fig.add_subplot(len(self.sample_list), 1, num + 1)

            for chrom_line in chrom_lines:
                ax.axvline(x=chrom_line, color="#000000", linewidth=1)
            for hl in [1, 2, 3, 4, 5, 6]:
                ax.axhline(y=hl, color="#000000", linewidth=1, linestyle="--")

            ax.plot(
                self.ratio_df['abspos'], self.ratio_df[sample],
                color="#bbbbbb", alpha=0.8)
            ax.plot(
                self.seg_df['abspos'], self.seg_df[sample],
                color='b', alpha=0.8)
            ax.set_yscale('log')

            ax.set_xlim((0, self.ratio_df['abspos'].values[-1]))
            ax.set_ylim((0.05, 20))

            ploidy = 0
            error = 0
            shredded = 0

            ax.set_title(
                sample + " Ploidy=" + ("%.2f" % ploidy) +
                         " Error=" + ("%.2f" % error) +
                         " Shredded=" + ("%.2f" % shredded))

            ax.set_xticks([])
            ax.set_xticklabels([])

            chrom_labels_pos = self.calc_chrom_labels_pos(chrom_lines)
            for num, label_pos in enumerate(chrom_labels_pos):
                ax.text(
                    label_pos, 10, self.CHROM_LABELS[num],
                    fontsize=10, horizontalalignment='center')


def main_sampleviewer():
    seg_filename = \
        'tests/data/sample.YL2671P11.5k.seg.quantal.primary.txt'
    seg_df = load_df(seg_filename)

    assert seg_df is not None

    ratio_filename = \
        'tests/data/sample.YL2671P11.5k.lowratio.quantal.primary.txt'
    ratio_df = load_df(ratio_filename)

    assert ratio_df is not None

    viewer = SampleViewer(seg_df, ratio_df, ['CTB4543'])
    viewer.draw_samples()

    plt.show()


if __name__ == '__main__':
    # main_heatmap()
    main_sampleviewer()

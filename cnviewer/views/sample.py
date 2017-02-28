'''
Created on Dec 14, 2016

@author: lubo
'''
import numpy as np
from views.base import ViewerBase
import webbrowser


class SamplesViewer(ViewerBase):

    def __init__(self, model):
        super(SamplesViewer, self).__init__(model)
        self.start_pos = None
        self.end_pos = None

    def calc_chrom_lines(self):
        return self.model.calc_chrom_lines()

    def calc_ploidy(self, sample_name):
        return self.model.data\
            .seg_df[sample_name]\
            .iloc[:self.model.chrom_x_index]\
            .mean()

    def upto_chrom_x(self, data):
        assert len(data) == len(self.model.data.seg_df)
        return data[0:self.model.chrom_x_index]

    def calc_error(self, sample_name):
        if self.model.data.ratio_df is None:
            return np.NaN
        df_r = self.upto_chrom_x(self.model.data.ratio_df[sample_name].values)
        df_s = self.upto_chrom_x(self.model.data.seg_df[sample_name].values)
        return np.sqrt(np.sum(((df_r - df_s) / df_s)**2))

    def calc_shredded(self, sample_name):
        upto_x_data = \
            self.model.data \
            .seg_df[sample_name].values[0:self.model.chrom_x_index]
        shredded = np.sum(upto_x_data < 0.4) / float(self.model.chrom_x_index)
        return shredded

    def draw_samples(self, fig, sample_list):

        self.chrom_lines = self.calc_chrom_lines()

        ax_common = None
        for num, sample_name in enumerate(sample_list):
            if num == 0:
                ax = fig.add_subplot(len(sample_list), 1, num + 1)
                ax_common = ax
            else:
                ax = fig.add_subplot(
                    len(sample_list), 1, num + 1,
                    sharex=ax_common,
                    sharey=ax_common)

            for chrom_line in self.chrom_lines:
                ax.axvline(x=chrom_line, color="#000000", linewidth=1)
            for hl in [1, 2, 3, 4, 5, 6]:
                ax.axhline(y=hl, color="#000000", linewidth=1, linestyle="--")

            if self.model.data.ratio_df is not None:
                ax.plot(
                    self.model.ratio_df['abspos'],
                    self.model.ratio_df[sample_name],
                    color="#bbbbbb", alpha=0.8)
            ax.plot(
                self.model.data.seg_df['abspos'],
                self.model.data.seg_df[sample_name],
                color='b', alpha=0.8)
            ax.set_yscale('log')

            ax.set_xlim((0, self.model.data.seg_df['abspos'].values[-1]))
            ax.set_ylim((0.05, 20))

            ploidy = self.calc_ploidy(sample_name)
            error = self.calc_error(sample_name)
            shredded = self.calc_shredded(sample_name)

            ax.set_title(
                "{} Ploidy={:.2f} Error={:.2f} Shredded={:.2f}".format(
                    sample_name, ploidy, error, shredded))

            ax.set_xticks([])
            ax.set_xticklabels([])

            chrom_labels_pos = self.calc_chrom_labels_pos(self.chrom_lines)
            ax.set_xticks(chrom_labels_pos)
            ax.set_xticklabels(self.CHROM_LABELS, rotation='vertical')

        fig.canvas.mpl_connect('button_press_event', self.event_handler)
        fig.canvas.mpl_connect('key_press_event', self.event_handler)
        fig.canvas.mpl_connect('button_release_event', self.event_handler)

    def event_handler(self, event):
        # self.debug_event(event)
        if event.name == 'button_press_event' and event.button == 3:
            pos = self.translate_xcoord(event.xdata)
            if self.start_pos is None:
                self.start_pos = pos
            else:
                self.end_pos = pos
                self.open_genome_browser()

    def translate_xcoord(self, xdata):
        index = np.abs(self.model.data.seg_df.abspos.values - xdata).argmin()
        chrom, chrompos = self.model.data.seg_df.iloc[index, [0, 1]]
        return (int(chrom), int(chrompos))

    def open_genome_browser(self):
        if self.start_pos is None or self.end_pos is None:
            return
        if self.start_pos[0] != self.end_pos[0]:
            self.start_pos = None
            self.end_pos = None
            return
        chrom = self.start_pos[0]
        if chrom == 23:
            chrom = 'X'
        if chrom == 24:
            chrom = 'Y'
        position = 'chr{}:{}-{}'.format(
            chrom, self.start_pos[1], self.end_pos[1])
        url = "http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position={}"\
            .format(position)
        print('opening url: ', url)
        webbrowser.open(url, new=False, autoraise=True)
        self.start_pos = None
        self.end_pos = None

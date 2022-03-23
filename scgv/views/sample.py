'''
Created on Dec 14, 2016

@author: lubo
'''
import numpy as np
from scgv.views.base import ViewerBase


class SamplesViewer(ViewerBase):

    def __init__(self, model):
        super(SamplesViewer, self).__init__(model)

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
                    self.model.data.ratio_df['abspos'],
                    self.model.data.ratio_df[sample_name],
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

            assert len(chrom_labels_pos) <= len(self.CHROM_LABELS)
            chrom_labels = self.CHROM_LABELS[:len(chrom_labels_pos)]

            ax.set_xticks(chrom_labels_pos)
            ax.set_xticklabels(chrom_labels, rotation='vertical')
        fig.tight_layout()

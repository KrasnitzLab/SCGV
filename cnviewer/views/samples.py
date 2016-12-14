'''
Created on Dec 14, 2016

@author: lubo
'''
import numpy as np
import matplotlib.pyplot as plt
from views.base import ViewerBase


class SampleViewer(ViewerBase):

    def __init__(self, seg_df, ratio_df):
        self.seg_df = seg_df
        self.ratio_df = ratio_df
        self.seg_data = seg_df.ix[:, 3:].values
        self.ratio_data = ratio_df.ix[:, 3:].values

    def calc_chrom_lines(self):
        chrom_lines = self.calc_chrom_lines_pos(self.seg_df)
        return self.seg_df['abspos'][chrom_lines]

    def calc_ploidy(self, sample_name):
        return self.seg_df[sample_name].mean()

    @property
    def chrom_x_index(self):
        index = np.where(self.seg_df['chrom'] == 23)[0][0]
        return index

    def upto_chrom_x(self, data):
        assert len(data) == len(self.seg_df)
        return data[0:self.chrom_x_index]

    def calc_error(self, sample_name):
        df_r = self.upto_chrom_x(self.ratio_df[sample_name].values)
        df_s = self.upto_chrom_x(self.seg_df[sample_name].values)
        return np.sqrt(np.sum(((df_r - df_s) / df_s)**2))

    def calc_shredded(self, sample_name):
        upto_x_data = self.seg_df[sample_name].values[0:self.chrom_x_index]
        shredded = np.sum(upto_x_data < 0.4) / float(self.chrom_x_index)
        return shredded

    def draw_samples(self, sample_list):
        fig = plt.figure(figsize=(12, 8))

        chrom_lines = self.calc_chrom_lines()

        for num, sample_name in enumerate(sample_list):
            ax = fig.add_subplot(len(sample_list), 1, num + 1)

            for chrom_line in chrom_lines:
                ax.axvline(x=chrom_line, color="#000000", linewidth=1)
            for hl in [1, 2, 3, 4, 5, 6]:
                ax.axhline(y=hl, color="#000000", linewidth=1, linestyle="--")

            ax.plot(
                self.ratio_df['abspos'], self.ratio_df[sample_name],
                color="#bbbbbb", alpha=0.8)
            ax.plot(
                self.seg_df['abspos'], self.seg_df[sample_name],
                color='b', alpha=0.8)
            ax.set_yscale('log')

            ax.set_xlim((0, self.ratio_df['abspos'].values[-1]))
            ax.set_ylim((0.05, 20))

            ploidy = self.calc_ploidy(sample_name)
            error = self.calc_error(sample_name)
            shredded = self.calc_shredded(sample_name)

            ax.set_title(
                "{} Ploidy={:.2f} Error={:.2f} Shredded={:.2f}".format(
                    sample_name, ploidy, error, shredded))

            ax.set_xticks([])
            ax.set_xticklabels([])

            chrom_labels_pos = self.calc_chrom_labels_pos(chrom_lines)
            for num, label_pos in enumerate(chrom_labels_pos):
                ax.text(
                    label_pos, 10, self.CHROM_LABELS[num],
                    fontsize=10, horizontalalignment='center')
        plt.show()

'''
Created on Dec 14, 2016

@author: lubo
'''
import numpy as np


class ViewerBase(object):
    NORMALIZE_MIN = 0
    NORMALIZE_MAX = 4
    CHROM_LABELS = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
        "14", "15", "16", "17", "18", "19", "20", "21", "22", "X", "Y"
    ]

    PLOIDY_LABELS = ["<2C", "2C", ">2C-4C", "4C", ">4C"]

    def __init__(self, model):
        self.model = model

    @staticmethod
    def calc_chrom_labels_pos(chrom_lines):
        yt = (np.roll(chrom_lines, -1) - chrom_lines) / 2.0
        return (chrom_lines + yt)[:-1]

    def clear_xlabels(self, ax):
        ax.set_xticks(self.model.label_midpoints)
        ax.set_xticklabels([''] * len(self.model.column_labels))

    def draw_xlabels(self, ax):
        ax.set_xticks(self.model.label_midpoints)
        ax.set_xticklabels(self.model.column_labels,
                           rotation='vertical',
                           fontsize=10)

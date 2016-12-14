'''
Created on Dec 14, 2016

@author: lubo
'''
import numpy as np


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

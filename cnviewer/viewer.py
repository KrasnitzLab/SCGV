'''
Created on Dec 2, 2016

@author: lubo
'''

import matplotlib.pyplot as plt

from utils.loader import load_df
from views.heatmap import HeatmapViewer
from views.samples import SampleViewer


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


def main_sampleviewer():
    seg_filename = \
        'tests/data/sample.YL2671P11.5k.seg.quantal.primary.txt'
    seg_df = load_df(seg_filename)

    assert seg_df is not None

    ratio_filename = \
        'tests/data/sample.YL2671P11.5k.lowratio.quantal.primary.txt'
    ratio_df = load_df(ratio_filename)

    assert ratio_df is not None

    viewer = SampleViewer(seg_df, ratio_df, ['CTB4517', 'CTB4543'])
    viewer.draw_samples()

    plt.show()


if __name__ == '__main__':
    # main_heatmap()
    main_sampleviewer()

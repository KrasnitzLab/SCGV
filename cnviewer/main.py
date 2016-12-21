'''
Created on Dec 2, 2016

@author: lubo
'''

import matplotlib.pyplot as plt

from utils.loader import load_df
from views.heatmap import HeatmapViewer
from views.samples import SampleViewer
from views.dendrogram import DendrogramViewer
from views.controller import HeatmapController
from views.clone import CloneViewer
from views.ploidy import PloidyViewer
from views.multiplier import MultiplierViewer
from views.error import ErrorViewer
from utils.model import DataModel


def main_heatmap():
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    model.make()

    viewer = HeatmapViewer(model)

    fig = plt.figure(0, figsize=(12, 8))

    ax_heat = fig.add_axes(
        [0.1, 0.10, 0.8, 0.65], frame_on=True)
    viewer.draw_heatmap(ax_heat)
    viewer.draw_legend()

    plt.show()


def main_sample():
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


def main_dendrogram():
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    model.make()

    fig = plt.figure(0, figsize=(12, 8))

    viewer = DendrogramViewer(model)
    ax_dendro = fig.add_axes([0.1, 0.75, 0.8, 0.2], frame_on=True)
    viewer.draw_dendrogram(ax_dendro)
    # viewer.draw_labels(ax_dendro)

    plt.show()


def main_controller():
    seg_filename = \
        'tests/data/uber.YL2671P5_CORE_F.5k.seg.quantal.primary.csv'
    seg_df = load_df(seg_filename)
    assert seg_df is not None

    tree_filename = \
        'tests/data/YL2671P5smear1bpFisherTreePyP4Cols.csv'
    tree_df = load_df(tree_filename)
    assert tree_df is not None

    ratio_filename = \
        'tests/data/uber.YL2671P5_CORE_F.5k.lowratio.quantal.primary.csv'
    ratio_df = load_df(ratio_filename)

    assert ratio_df is not None

    sample_viewer = SampleViewer(seg_df, ratio_df)

    fig = plt.figure(0, figsize=(12, 8))
    fig.suptitle(seg_filename, fontsize=10)

    heatmap_viewer = HeatmapViewer(seg_df, tree_df)
    heatmap_viewer.draw()

    controller = HeatmapController(heatmap_viewer, sample_viewer)
    controller.event_loop_connect(fig)

    plt.show()


def main_clone():
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    model.make()

    clone = CloneViewer(model)
    fig = plt.figure(0, figsize=(12, 8))
    ax_clone = fig.add_axes(
        [0.1, 0.7625, 0.8, 0.0125], frame_on=True)
    clone.draw_clone(ax_clone)
    ax_subclone = fig.add_axes(
        [0.1, 0.75, 0.8, 0.0125], frame_on=True)
    clone.draw_subclone(ax_subclone)

    plt.show()


def main_ploidy():
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    model.make()

    ploidy = PloidyViewer(model)

    fig = plt.figure(0, figsize=(12, 8))
    ax_ploidy = fig.add_axes(
        [0.1, 0.7625, 0.8, 0.0125], frame_on=True)
    ploidy.draw_ploidy(ax_ploidy)

    plt.show()


def main_error_and_multiplier():
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    model.make()

    multiplier = MultiplierViewer(model)
    fig = plt.figure(0, figsize=(12, 8))

    ax_multiplier = fig.add_axes(
        [0.1, 0.125, 0.8, 0.025], frame_on=True)
    multiplier.draw_multiplier(ax_multiplier)

    error = ErrorViewer(model)
    ax_error = fig.add_axes(
        [0.1, 0.10, 0.8, 0.025], frame_on=True)
    error.draw_error(ax_error)

    plt.show()


if __name__ == '__main__':
    main_heatmap()
    # main_sample()
    # main_dendrogram()
    # main_controller()
    # main_clone()
    # main_ploidy()
    # main_error_and_multiplier()

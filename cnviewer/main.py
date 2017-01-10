'''
Created on Dec 2, 2016

@author: lubo
'''

import matplotlib.pyplot as plt

from views.heatmap import HeatmapViewer
from views.sample import SampleViewer
from views.dendrogram import DendrogramViewer
from views.controller import MainController
from views.clone import CloneViewer
from views.gate import GateViewer
from views.multiplier import MultiplierViewer
from views.error import ErrorViewer
from utils.model import DataModel
from utils.sector_model import SectorDataModel


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
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    model.make()

    viewer = SampleViewer(model)
    viewer.draw_samples(['CTB6991.', 'CTB6994.'])

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

    gate = GateViewer(model)

    fig = plt.figure(0, figsize=(12, 8))
    ax_ploidy = fig.add_axes(
        [0.1, 0.7625, 0.8, 0.0125], frame_on=True)
    gate.draw_ploidy(ax_ploidy)

    plt.show()


def main_error_and_multiplier():
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    model.make()

    multiplier = MultiplierViewer(model)
    fig = plt.figure(0, figsize=(12, 10))

    ax_multiplier = fig.add_axes(
        [0.1, 0.125, 0.8, 0.025], frame_on=True)
    multiplier.draw_multiplier(ax_multiplier)

    error = ErrorViewer(model)
    ax_error = fig.add_axes(
        [0.1, 0.10, 0.8, 0.025], frame_on=True)
    error.draw_error(ax_error)

    plt.show()


def main_controller():
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    model.make()

    mfig = plt.figure(0, figsize=(12, 8))
    mfig.suptitle("seg", fontsize=14)
    main = MainController(model)
    main.build_main(mfig)

    pfig = plt.figure(1, figsize=(12, 8))
    pfig.suptitle("pinmat", fontsize=14)
    pinmat = MainController(model)
    pinmat.build_pinmat(pfig)

    sfig = plt.figure(2, figsize=(12, 8))
    sfig.suptitle("sector", fontsize=14)
    sector_model = SectorDataModel(model)
    sector_model.make()
    sector = MainController(sector_model)
    sector.build_sector(sfig)

    plt.show()


if __name__ == '__main__':
    # main_heatmap()
    # main_sample()
    # main_dendrogram()
    # main_clone()
    # main_ploidy()
    # main_error_and_multiplier()
    main_controller()

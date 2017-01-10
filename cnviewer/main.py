'''
Created on Dec 2, 2016

@author: lubo
'''

import matplotlib.pyplot as plt

from views.controller import MainController
from utils.model import DataModel
from utils.sector_model import SectorDataModel


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
    main_controller()

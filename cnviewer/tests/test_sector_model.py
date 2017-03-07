'''
Created on Jan 18, 2017

@author: lubo
'''
import numpy as np

from models.sector_model import SectorsDataModel, SingleSectorDataModel
from models.model import DataModel


def test_data_model_make_01():
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    assert model is not None
    model.make()

    sector_model = SectorsDataModel(model)
    sector_model.make()

    print(sector_model.column_labels)
    print(sector_model.sector)

    print(np.argwhere(43 == model.Z['leaves']))

    print(np.argmin(model.sector))
    m = np.argmin(model.sector)
    print(m)
    print(model.sector[m])
    print(model.column_labels[m])

    print(m - 1)
    print(model.sector[m - 1])
    print(model.column_labels[m - 1])

    assert sector_model.sector[0] == 1
    assert sector_model.column_labels[0] == model.column_labels[m]


def test_sector_order_experiments():
    elements = np.array([0, 1, 2, 3])
    leaves = np.array([3, 1, 2, 0])
    sectors = np.array([1, 1, 2, 2])

    res = np.lexsort(
        (
            leaves,
            sectors
        )
    )

    print(elements[res])
    print(elements[leaves])

    assert np.all(elements[res] == np.array([1, 0, 3, 2]))

SECTOR_5_LMM_LMAT = np.array([
    [8.0, 20.0, 119.11823367520807, 31.0],
    [21.0, 11.0, 123.56298739803918, 36.0],
    [0.0, 17.0, 123.95887662779884, 5.0],
    [19.0, 7.0, 124.07883294268733, 35.0],
    [1.0, 3.0, 124.08988731420767, 13.0],
    [24.0, 25.0, 124.09265019905367, 54.0],
    [5.0, 23.0, 124.10510570864511, 33.0],
    [22.0, 26.0, 124.11337004932325, 112.0],
    [16.0, 28.0, 124.12237557847548, 119.0],
    [27.0, 29.0, 124.1295443777383, 157.0],
    [15.0, 30.0, 124.14564121314146, 172.0],
    [14.0, 31.0, 124.15486242434721, 179.0],
    [18.0, 32.0, 124.15820050018895, 190.0],
    [2.0, 33.0, 124.20542282820034, 220.0],
    [4.0, 34.0, 124.20542282820034, 228.0],
    [6.0, 35.0, 124.20542282820034, 232.0],
    [9.0, 36.0, 124.20542282820034, 239.0],
    [10.0, 37.0, 124.20542282820034, 241.0],
    [12.0, 38.0, 124.20542282820034, 243.0],
    [13.0, 39.0, 124.20542282820034, 245.0]
])


def test_single_sector_subtree_experiments():
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    assert model is not None
    model.make()
    print(model.sector_mapping)

    single_sector_model = SingleSectorDataModel(model, ' 5 LMM')
    single_sector_model.make()

    lmat = np.array(single_sector_model.lmat)
    print(lmat[:, 0])
    print(lmat[:, 1])

    assert np.all(SECTOR_5_LMM_LMAT[:, 0] == lmat[:, 0])
    assert np.all(SECTOR_5_LMM_LMAT[:, 1] == lmat[:, 1])


def test_single_sector_subtree_twice():
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    assert model is not None
    model.make()
    print(model.sector_mapping)

    single_sector_model = SingleSectorDataModel(model, ' 5 LMM')
    single_sector_model.make()

    lmat = np.array(single_sector_model.lmat)
    print(lmat[:, 0])
    print(lmat[:, 1])

    assert np.all(SECTOR_5_LMM_LMAT[:, 0] == lmat[:, 0])
    assert np.all(SECTOR_5_LMM_LMAT[:, 1] == lmat[:, 1])

    single_sector_model = SingleSectorDataModel(model, ' 5 LMM')
    single_sector_model.make()

    lmat = np.array(single_sector_model.lmat)
    print(lmat[:, 0])
    print(lmat[:, 1])

    assert np.all(SECTOR_5_LMM_LMAT[:, 0] == lmat[:, 0])
    assert np.all(SECTOR_5_LMM_LMAT[:, 1] == lmat[:, 1])

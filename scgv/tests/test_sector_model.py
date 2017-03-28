'''
Created on Jan 18, 2017

@author: lubo
'''
import numpy as np

from models.sector_model import SectorsDataModel, SingleSectorDataModel
from models.model import DataModel


def test_data_model_make_01():
    model = DataModel('../exampledata/example.archive.zip')
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


def test_single_sector_subtree_experiments():
    model = DataModel('../exampledata/example.archive.zip')
    assert model is not None
    model.make()
    print(model.sector_mapping)

    single_sector_model = SingleSectorDataModel(model, 1)
    single_sector_model.make()

    lmat = np.array(single_sector_model.lmat)
    print(lmat[:, 0])
    print(lmat[:, 1])


def test_single_sector_subtree_twice():
    model = DataModel('../exampledata/example.archive.zip')
    assert model is not None
    model.make()
    print(model.sector_mapping)

    single_sector_model = SingleSectorDataModel(model, 1)
    single_sector_model.make()

    lmat = np.array(single_sector_model.lmat)
    print(lmat[:, 0])
    print(lmat[:, 1])

    single_sector_model = SingleSectorDataModel(model, 1)
    single_sector_model.make()

    lmat = np.array(single_sector_model.lmat)
    print(lmat[:, 0])
    print(lmat[:, 1])

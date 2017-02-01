'''
Created on Jan 18, 2017

@author: lubo
'''
import numpy as np

from utils.sector_model import SectorDataModel
from utils.model import DataModel


def test_data_model_make_01():
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    assert model is not None
    model.make()

    sector_model = SectorDataModel(model)
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

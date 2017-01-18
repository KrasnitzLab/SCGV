'''
Created on Jan 18, 2017

@author: lubo
'''
from utils.sector_model import SectorDataModel
from utils.model import DataModel


def test_data_model_make_01():
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    assert model is not None
    model.make()

    sector_model = SectorDataModel(model)
    sector_model.build_ordering()

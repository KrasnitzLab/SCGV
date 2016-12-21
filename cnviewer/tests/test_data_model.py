'''
Created on Dec 21, 2016

@author: lubo
'''
from utils.model import DataModel


def test_data_model_create():

    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    assert model is not None


def test_data_model_make():
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    model.make()

'''
Created on Dec 21, 2016

@author: lubo
'''
from utils.model import DataModel
# import pytest


def test_data_model_create():

    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    assert model is not None


def test_data_model_make():
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    model.make()


def test_data_model_make_01():
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    assert model is not None
    # model.make()


def test_make_pinmap():
    model = DataModel('tests/data/cnviewer_data_example_00.zip')
    assert model is not None

    model.make_linkage()
    model.make_dendrogram()
    model.make_pinmat()

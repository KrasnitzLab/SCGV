'''
Created on Dec 21, 2016

@author: lubo
'''
from utils.loader import DataLoader
import pytest


def test_data_loader_bad_filename():
    with pytest.raises(AssertionError):
        DataLoader("ala_bala.zip")


def test_data_loader_bad_zip():
    with pytest.raises(AssertionError):
        DataLoader("tests/data/tbguide.csv")


def test_data_loader_create_00():
    loader = DataLoader('tests/data/cnviewer_data_example_00.zip')
    assert loader is not None
    print(loader.keys())


# @pytest.mark.xfail
def test_data_loader_create_01():
    loader = DataLoader('tests/data/cnviewer_data_example_01.zip')
    assert loader is not None
    print(loader.keys())

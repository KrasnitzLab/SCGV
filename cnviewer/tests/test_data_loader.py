'''
Created on Dec 21, 2016

@author: lubo
'''
from models.loader import DataLoader
import pytest


def test_data_loader_bad_filename():
    with pytest.raises(AssertionError):
        DataLoader("ala_bala.zip").load()


def test_data_loader_bad_zip():
    with pytest.raises(AssertionError):
        DataLoader("tests/data/tbguide.csv").load()


def test_data_zip_loader_create_01():
    loader = DataLoader('tests/data/cnviewer_data_example_01.zip')
    loader.load()

    assert loader is not None
    print(loader.data.keys())


@pytest.mark.xfail
def test_data_dir_loader_create_01():
    loader = DataLoader('tests/data/cnviewer_data_example_01')
    assert loader is not None
    print(loader.keys())


@pytest.mark.xfail
def test_data_loader_create_02():
    loader = DataLoader('tests/data/example02.named.zip')
    assert loader is not None
    print(loader.keys())


def test_data_load_minimal_dataset():
    loader = DataLoader('tests/data/cnviewer_data_example_02.zip')
    loader.load()
    print(loader.data.keys())

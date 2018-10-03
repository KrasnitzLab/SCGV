'''
Created on Dec 21, 2016

@author: lubo
'''
from scgv.models.loader import DataLoader
import pytest


def test_data_loader_bad_filename():
    with pytest.raises(AssertionError):
        DataLoader("ala_bala.zip").load()


def test_data_loader_bad_zip():
    with pytest.raises(AssertionError):
        DataLoader("tests/data/tbguide.csv").load()


def test_data_zip_loader_create_01(example_dir):
    loader = DataLoader(example_dir)
    loader.load()

    assert loader is not None


def test_data_dir_loader_create_01(example_dir):
    loader = DataLoader(example_dir)
    loader.load()
    assert loader is not None

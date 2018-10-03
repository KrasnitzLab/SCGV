'''
Created on Dec 2, 2016

@author: lubo
'''
import pytest
from scgv.models.model import DataModel


@pytest.fixture
def example_data():
    return 'exampledata/example.archive.zip'


@pytest.fixture
def example_dir():
    return 'exampledata/example.directory'


@pytest.fixture
def model_fixture(example_data):
    model = DataModel(example_data)
    model.make()
    return model

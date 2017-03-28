'''
Created on Dec 2, 2016

@author: lubo
'''
import pytest
from models.model import DataModel


@pytest.fixture(scope='session')
def model_fixture(request):
    model = DataModel('../exampledata/example.archive.zip')
    model.make()
    return model

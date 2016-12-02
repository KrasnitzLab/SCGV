'''
Created on Dec 2, 2016

@author: lubo
'''
import pytest
import os


@pytest.fixture(scope='session')
def seg_filename(request):
    filename = "tests/data/sample.YL2671P11.5k.seg.quantal.primary.txt"
    assert os.path.isfile(filename)
    return filename


@pytest.fixture(scope='session')
def ratio_filename(request):
    filename = "tests/data/sample.YL2671P11.5k.lowratio.quantal.primary.txt"
    assert os.path.isfile(filename)
    return filename

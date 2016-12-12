'''
Created on Dec 2, 2016

@author: lubo
'''
import pytest
import os
from utils.loader import load_df
from viewer import Viewer


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


@pytest.fixture(scope='session')
def viewer(request, seg_filename):
    seg_filename = 'tests/data/sample.YL2671P11.5k.seg.quantal.primary.txt'
    df = load_df(seg_filename)
    viewer = Viewer(df)
    viewer.make_linkage()
    viewer.make_dendrogram(ax=None, no_plot=True)

    return viewer

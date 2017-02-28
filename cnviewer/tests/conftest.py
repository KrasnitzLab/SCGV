'''
Created on Dec 2, 2016

@author: lubo
'''
import pytest
import os
from models.loader import load_df
from views.heatmap import HeatmapViewer
from views.sample import SamplesViewer
from models.model import DataModel


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
def seg_df(request, seg_filename):
    df = load_df(seg_filename)
    return df


@pytest.fixture(scope='session')
def ratio_df(request, ratio_filename):
    df = load_df(ratio_filename)
    return df


@pytest.fixture(scope='session')
def heatmap(request, seg_filename):
    df = load_df(seg_filename)
    viewer = HeatmapViewer(df)
    viewer.make_linkage(None)
    viewer.make_dendrogram()

    return viewer


@pytest.fixture(scope='session')
def sample_viewer(request, seg_df, ratio_df):
    viewer = SamplesViewer(seg_df, ratio_df)

    return viewer


@pytest.fixture(scope='session')
def model_fixture(request):
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    model.make()
    return model

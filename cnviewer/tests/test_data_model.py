'''
Created on Dec 21, 2016

@author: lubo
'''
import numpy as np
from models.model import DataModel  # , gate_compare
from models.featuremat_model import FeaturematModel
# import pytest


def test_data_model_make_01():
    model = DataModel('../exampledata/example.archive.zip')
    assert model is not None
    model.make()

    sectors_legend = model.make_sectors_legend()
    print(sectors_legend)


def test_make_featuremat():
    model = DataModel('../exampledata/example.archive.zip')
    assert model is not None

    model.make()

    featuremat_model = FeaturematModel(model)
    featuremat_model.make()


def test_convolution():
    a = np.array([0, 0, 0, 0, -1, 0, 1, 0, 0])
    b = np.array([1, 1, 1])

    c = np.convolve(a, b)
    print(c)

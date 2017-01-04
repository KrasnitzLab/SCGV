'''
Created on Jan 4, 2017

@author: lubo
'''
import numpy as np

from views.sample import SampleViewer
import pytest


def test_multiplier(model_fixture):
    sample = SampleViewer(model_fixture)
    assert sample is not None

    sample_name = 'CJA4006'
    assert sample_name in model_fixture.column_labels

    m1 = sample.calc_ploidy(sample_name)

    sample_index = np.where(model_fixture.column_labels == sample_name)
    m2 = model_fixture.multiplier[sample_index]
    assert len(m2) == 1

    print(m1, m2[0])

    assert m1 == pytest.approx(m2[0], abs=1E-6)


def test_all_mutipliers(model_fixture):
    sample = SampleViewer(model_fixture)

    for sample_name in model_fixture.column_labels:
        m1 = sample.calc_ploidy(sample_name)

        sample_index = np.where(model_fixture.column_labels == sample_name)
        m2 = model_fixture.multiplier[sample_index]
        assert len(m2) == 1

        assert m1 == pytest.approx(m2[0], abs=1E-6)


def test_error(model_fixture):
    sample = SampleViewer(model_fixture)
    assert sample is not None

    sample_name = 'CJA4006'
    assert sample_name in model_fixture.column_labels

    e1 = sample.calc_error(sample_name)

    sample_index = np.where(model_fixture.column_labels == sample_name)
    e2 = model_fixture.error[sample_index]
    assert len(e2) == 1

    print(e1, e2[0])

    assert e1 == pytest.approx(e2[0], abs=1E-6)


def test_all_errors(model_fixture):
    sample = SampleViewer(model_fixture)

    for sample_name in model_fixture.column_labels:
        e1 = sample.calc_error(sample_name)

        sample_index = np.where(model_fixture.column_labels == sample_name)
        e2 = model_fixture.error[sample_index]
        assert len(e2) == 1
        assert e1 == pytest.approx(e2[0], abs=1E-6)

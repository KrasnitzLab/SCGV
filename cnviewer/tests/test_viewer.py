'''
Created on Dec 12, 2016

@author: lubo
'''
import mock
import pytest


def test_column_labels(heatmap):
    assert heatmap is not None
    assert heatmap.Z is not None

    assert 'CTB4517' == heatmap.column_labels[0]
    assert 'CTB4543' == heatmap.column_labels[54]


def test_locate_sample_click(heatmap):
    event = mock.MagicMock()
    event.xdata = 1

    sample = heatmap.locate_sample_click(event)
    assert 'CTB4517' == sample


def test_upto_chrom_x(sample_viewer, seg_df):
    assert sample_viewer is not None

    df = sample_viewer.upto_chrom_x(seg_df)
    assert df is not None
    assert len(df) < len(seg_df)
    assert 4724 == len(df)


def test_calc_error(sample_viewer):
    error = sample_viewer.calc_error('CTB4517')
    assert pytest.approx(39.77, abs=1e-2) == error

    error = sample_viewer.calc_error('CTB4543')
    assert pytest.approx(18.88, abs=1e-2) == error


def test_calc_ploidy(sample_viewer):
    ploidy = sample_viewer.calc_ploidy('CTB4517')
    assert pytest.approx(1.75, abs=1e-2) == ploidy

    ploidy = sample_viewer.calc_ploidy('CTB4543')
    assert pytest.approx(3.66, abs=1e-2) == ploidy


def test_calc_shredded(sample_viewer):
    shredded = sample_viewer.calc_shredded('CTB4517')
    assert pytest.approx(0.27, abs=1e-2) == shredded

    shredded = sample_viewer.calc_shredded('CTB4543')
    assert pytest.approx(0.0, abs=1e-2) == shredded

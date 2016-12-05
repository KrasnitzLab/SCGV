'''
Created on Dec 2, 2016

@author: lubo
'''
import pandas as pd
import pytest


def test_seg_filename_fixture(seg_filename):
    assert seg_filename is not None


def test_ratio_filename_fixture(ratio_filename):
    assert ratio_filename is not None


def test_seq_df(seg_filename):
    df = pd.read_csv(seg_filename, sep='\t')
    assert df is not None
    assert len(df) == 5000

    assert 'chrom' in df.columns
    assert 'chrompos' in df.columns
    assert 'abspos' in df.columns


def test_ratio_df(ratio_filename):
    df = pd.read_csv(ratio_filename, sep='\t')
    assert df is not None
    assert len(df) == 5000

    assert 'chrom' in df.columns
    assert 'chrompos' in df.columns
    assert 'abspos' in df.columns


@pytest.mark.xfail
def test_seg_df_data(seg_filename):
    df = None
    assert df is not None

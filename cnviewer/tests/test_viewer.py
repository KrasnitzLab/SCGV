'''
Created on Dec 12, 2016

@author: lubo
'''
import mock


def test_column_labels(viewer):
    assert viewer is not None
    assert viewer.Z is not None

    assert 'CTB4517' == viewer.column_labels[0]
    assert 'CTB4543' == viewer.column_labels[54]


def test_locate_sample_click(viewer):
    event = mock.MagicMock()
    event.xdata = 1

    sample = viewer.locate_sample_click(event)
    assert 'CTB4517' == sample

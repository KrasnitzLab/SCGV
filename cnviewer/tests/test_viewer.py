'''
Created on Dec 12, 2016

@author: lubo
'''


def test_column_labels(viewer):
    assert viewer is not None
    viewer.make_linkage()
    viewer.make_dendrogram(ax=None, no_plot=True)
    assert viewer.Z is not None

    assert 'CTB4517' == viewer.column_labels[0]
    assert 'CTB4543' == viewer.column_labels[54]

'''
Created on Dec 21, 2016

@author: lubo
'''
import numpy as np
from utils.model import DataModel  # , gate_compare
# import pytest


def test_data_model_make_01():
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    assert model is not None
    # model.make()


def test_make_pinmat():
    model = DataModel('tests/data/cnviewer_data_example_01.zip')
    assert model is not None

    model.make_linkage()
    ordering = model.make_dendrogram()
    model.make_pinmat(ordering=ordering)

#     expected = np.loadtxt('tests/data/pin_data_single.csv.gz',
#                           delimiter='\t')
#     assert expected is not None
#     print(expected.shape)
#     print(model.seg_data.shape)
#
#     count = 0
#     for i in xrange(model.bins):
#         for j in xrange(model.samples):
#             expected_val = expected[i, model.direct_lookup[j]]
#             if model.pins[i, j] != expected_val:
#                 label1 = model.column_labels[j]
#                 label2 = model.pinmat_df.columns[j]
#                 print(i, j, model.pins[i, j], expected_val, label1, label2)
#                 count += 1
#                 if count > 100:
#                     break
#         if count > 100:
#             break
#     print("total differences: {}".format(count))


#     assert model.pins[0, 72] == 1
#     assert model.pins[0, 107] == 1
#     assert model.pins[1, 1] == 1
#     assert model.pins[1, 12] == 1
#     assert model.pins[7, 1] == 1


def test_convolution():
    a = np.array([0, 0, 0, 0, -1, 0, 1, 0, 0])
    b = np.array([1, 1, 1])

    c = np.convolve(a, b)
    print(c)


# def test_gate_sort():
#     assert ['<2C', '>2C'] == sorted(['>2C', '<2C'], key=gate_compare)
#     assert ['<2C', '2C'] == sorted(['<2C', '2C'], key=gate_compare)
#     assert ['2C', '>2C'] == sorted(['>2C', '2C'], key=gate_compare)
#     assert ['2C', '3C', ] == sorted(['2C', '3C'], key=gate_compare)
#     assert ['3C', '>3C', ] == sorted(['>3C', '3C'], key=gate_compare)
#     assert ['<2C', '3C', ] == sorted(['<2C', '3C'], key=gate_compare)
#
#     gates = ['>2C', '2C Rt', '2C']
#     sorted_gates = sorted(gates, key=gate_compare)
#     assert ['2C', '2C Rt', '>2C'] == sorted_gates

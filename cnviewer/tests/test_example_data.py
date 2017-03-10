'''
Created on Mar 10, 2017

@author: lubo
'''


from models.loader import DataLoader


def test_load_example_data_dir():
    loader = DataLoader('tests/data/exampledata')
    loader.load()

    assert loader.cell_df is not None
    assert 'cells' in loader.data


def test_loader_filter_cells():
    loader = DataLoader('tests/data/exampledata')
    loader.load()

    loader.filter_cells()


def test_loader_order_cells():
    loader = DataLoader('tests/data/exampledata')
    loader.load()

    loader.filter_cells()
    loader.order_cells()

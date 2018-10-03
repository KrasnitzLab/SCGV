'''
Created on Mar 10, 2017

@author: lubo
'''


from scgv.models.loader import DataLoader


def test_load_example_data_dir(example_dir):
    loader = DataLoader(example_dir)
    loader.load()

    assert loader.cell_df is not None
    assert 'cells' in loader.data


def test_loader_filter_cells(example_data):
    loader = DataLoader(example_data)
    loader.load()

    loader.filter_cells()


def test_loader_order_cells(example_data):
    loader = DataLoader(example_data)
    loader.load()

    loader.filter_cells()
    loader.order_cells()

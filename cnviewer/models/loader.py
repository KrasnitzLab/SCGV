'''
Created on Dec 2, 2016

@author: lubo
'''
import numpy as np
import pandas as pd
import os
import zipfile

from PIL import Image


def load_df(filename):
    df = pd.read_csv(filename, sep='\t')
    return df


class DataLoader(object):
    TYPES = set([
        'ratio', 'pinmat', 'clone', 'tree', 'seg',
        'pins', 'guide', 'genome', 'cells'])
    GUIDE_SAMPLES_COLUMN = 'seq.unit.id'
    CLONE_ID_COLUMN = 'ID'

    def __init__(self, filename):
        self.pathology = None
        self.data = {}
        self.filename = filename

    def load(self):
        if os.path.isdir(self.filename):
            self._load_dir(self.filename)
        else:
            self._load_zipfile(self.filename)
        self.cell_df = self.data.get('cells', None)
        self.seg_df = self.data.get('seg', None)
        self.ratio_df = self.data.get('ratio', None)
        self.clone_df = self.data.get('clone', None)
        self.tree_df = self.data.get('tree', None)
        self.guide_df = self.data.get('guide', None)
        self.pinmat_df = self.data.get('pinmat', None)
        self.pins_df = self.data.get('pins', None)
        self.genome = self.data.get('genome', 'hg19')

        assert self.cell_df is not None
        assert self.seg_df is not None
        assert self.genome is not None

    @classmethod
    def _organize_filenames(cls, namelist):
        result = {}
        for filename in namelist:
            parts = filename.split('.')
            if len(parts) < 3:
                continue
            filetype = parts[-2]
            if filetype not in cls.TYPES:
                continue
            result[filetype] = filename
        return result

    def _load_zipfile(self, zip_filename):
        assert os.path.isfile(zip_filename)
        assert os.path.exists(zip_filename)
        assert zipfile.is_zipfile(zip_filename)
        with zipfile.ZipFile(zip_filename, 'r') as zipdata:
            filenames = self._organize_filenames(zipdata.namelist())
            assert 'seg' in set(filenames.keys())
            for filetype, filename in filenames.items():
                infile = zipdata.open(filename)
                if filetype == 'genome':
                    genome = self._load_genome_build(infile)
                    if genome:
                        self.data['genome'] = genome
                else:
                    df = pd.read_csv(infile, sep='\t')
                    assert df is not None
                    self.data[filetype] = df
            self.pathology = self._load_images_zipfile(zipdata)

    def _load_images_zipfile(self, zipdata):
        descriptor = 'pathology/description.csv'
        if descriptor not in zipdata.namelist():
            return
        infile = zipdata.open(descriptor)
        images_df = pd.read_csv(infile)

        result = {}
        for _index, row in images_df.iterrows():
            image = None
            if 'image' in row:
                filename = os.path.join('pathology', str(row['image']))
                if filename in zipdata.namelist():
                    image = Image.open(zipdata.open(filename))
                    # image.load()
            else:
                print("image not found: ", filename)

            notes = None
            if 'notes' in row:
                filename = os.path.join('pathology', str(row['notes']))
                if filename in zipdata.namelist():
                    notes = zipdata.open(filename).readlines()
                    # image.load()
                else:
                    print("image not found: ", filename)
            result[row['pathology']] = image, notes

        return result

    def _load_genome_build(self, infile):
        df = pd.read_csv(infile, sep=',')
        df = df[df['in_use'] == 1]
        if len(df) == 0:
            return None
        return df.id.values[0]

    def _load_dir(self, dir_filename):
        assert os.path.exists(dir_filename)
        assert os.path.isdir(dir_filename)
        all_filenames = [
            os.path.join(dir_filename, f) for f in os.listdir(dir_filename)
            if os.path.isfile(os.path.join(dir_filename, f))]
        filenames = self._organize_filenames(all_filenames)

        for filetype, filename in filenames.items():
            infile = open(filename)
            if filetype == 'genome':
                genome = self._load_genome_build(infile)
                if genome:
                    self.data['genome'] = genome
            else:
                df = pd.read_csv(infile, sep='\t')
                assert df is not None
                self.data[filetype] = df

        self.pathology = None
        pathology_dirname = os.path.join(dir_filename, 'pathology')
        if os.path.exists(pathology_dirname) and \
                os.path.isdir(pathology_dirname):
            self.pathology = self._load_pathology_dir(pathology_dirname)
        else:
            print('pathology directory not found: {}'.format(
                pathology_dirname))

    def _load_pathology_dir(self, pathology_dirname):
        filename = os.path.join(pathology_dirname, 'description.csv')
        images_df = pd.read_csv(filename)
        result = {}
        for _index, row in images_df.iterrows():
            image = None
            if 'image' in row:
                filename = os.path.join(pathology_dirname, str(row['image']))
                if os.path.exists(filename):
                    image = Image.open(filename)

            notes = None
            if 'notes' in row:
                filename = os.path.join(pathology_dirname, str(row['notes']))
                if os.path.exists(filename):
                    with open(filename, 'r') as notesfile:
                        notes = notesfile.readlines()
            result[row['pathology']] = image, notes
        return result

    def filter_and_order_cells(self):
        assert self.cell_df is not None

    def _filter_df_columns(self, df, keep=3):
        """
        used to filter columns in seg and ratio files.
        should keep first 3 columns intact
        """
        if keep:
            columns = list(df.columns[:keep])
        else:
            columns = []
        for c in df.columns[keep:]:
            if c in self.sample_names:
                columns.append(c)

        df = df.ix[:, columns].copy()
        return df

    def _filter_df_rows(self, df, cell_column):
        df = df[df[cell_column].isin(self.sample_names)].copy()
        df.reset_index(inplace=True)
        return df

    def filter_cells(self):
        assert self.cell_df is not None
        self.sample_names = set(self.cell_df.cell.values)

        assert self.seg_df is not None
        self.seg_df = self._filter_df_columns(self.seg_df)
        assert len(self.seg_df.columns) == len(self.sample_names) + 3

        if self.ratio_df is not None:
            self.ratio_df = self._filter_df_columns(self.ratio_df)
            assert len(self.ratio_df.columns) == len(self.sample_names) + 3

        if self.pinmat_df is not None:
            self.pinmat_df = self._filter_df_columns(self.pinmat_df, keep=0)
            assert len(self.pinmat_df.columns) == len(self.sample_names)

        if self.guide_df is not None:
            self.guide_df = self._filter_df_rows(
                self.guide_df, self.GUIDE_SAMPLES_COLUMN)
            assert len(self.guide_df) == len(self.sample_names)

        if self.clone_df is not None:
            self.clone_df = self._filter_df_rows(
                self.clone_df, self.CLONE_ID_COLUMN)
            assert len(self.clone_df) == len(self.sample_names)

        if self.tree_df is not None:
            assert len(self.sample_names) == len(self.tree_df) + 1, \
                "tree file size mismatched"
            self.tree_df = self.tree_df.ix[:, 0:4].copy()

    def order_cells(self):
        order = self.cell_df.cell.values
        self.seg_df = self._order_df_columns(order, self.seg_df, keep=3)
        assert np.all(self.seg_df.columns[3:] == order)

        if self.ratio_df is not None:
            self.ration_df = self._order_df_columns(
                order, self.ratio_df, 3)
            assert np.all(self.ratio_df.columns[3:] == order)

        if self.pinmat_df is not None:
            self.pinmat_df = self._order_df_columns(
                order, self.pinmat_df, 0)
            assert np.all(self.pinmat_df.columns == order)

        if self.guide_df is not None:
            self.guide_df = self._order_df_rows(
                order, self.guide_df, self.GUIDE_SAMPLES_COLUMN)
            assert np.all(
                order ==
                self.guide_df[self.GUIDE_SAMPLES_COLUMN].values
            )
        if self.clone_df is not None:
            self.clone_df = self._order_df_rows(
                order, self.clone_df, self.CLONE_ID_COLUMN)
            assert np.all(
                order ==
                self.clone_df[self.CLONE_ID_COLUMN])

    def _order_df_columns(self, order, df, keep):
        columns = df.columns[keep:]
        indices = self._sort_indices(order, columns) + keep
        prefix = np.arange(0, keep)
        indices = np.hstack((prefix, indices))
        assert len(indices) == len(df.columns)
        df = df.ix[:, indices]
        return df

    def _order_df_rows(self, order, df, col_name):
        indices = self._sort_indices(order, df[col_name].values)
        df = df.ix[indices, :]
        df.reset_index(inplace=True)
        return df

    def _sort_indices(self, order, npcells):
        cells = list(npcells)
        indices = []
        for cell in order:
            index = cells.index(cell)
            assert index >= 0
            indices.append(index)
        indices = np.array(indices)
        return indices

#     def filter_samples(self):
#         assert self.seg_df is not None
#
#         if self.pinmat_df is None:
#             return
#
#         self.sample_names = set(self.pinmat_df.columns)
#         seg_columns = list(self.seg_df.columns[:3])
#         for c in self.seg_df.columns[3:]:
#             if c in self.sample_names:
#                 seg_columns.append(c)
#
#         self.seg_df = self.seg_df.ix[:, seg_columns].copy()
#         self.data['seg'] = self.seg_df
#         assert len(self.seg_df.columns) == len(self.sample_names) + 3
#
#         if self.guide_df is not None:
#             self.guide_df = self.guide_df[self.guide_df[
#                 self.GUIDE_SAMPLES_COLUMN].isin(self.sample_names)].copy()
#             self.guide_df.reset_index(inplace=True)
#             self.data['guide'] = self.guide_df
#
#             assert len(self.sample_names) == len(self.guide_df)
#
#             assert set(self.pinmat_df.columns) == \
#                 set(self.guide_df[self.GUIDE_SAMPLES_COLUMN].values), \
#                 "guide file and pinmat file cells mismatched"
#             assert np.all(
#                 self.pinmat_df.columns ==
#                 self.guide_df[self.GUIDE_SAMPLES_COLUMN]), \
#                 "guide file and pinmat file cells ordering mismatched"
#
#             assert set(self.seg_df.columns[3:]) == \
#                 set(self.guide_df[self.GUIDE_SAMPLES_COLUMN].values), \
#                 "guide file and seg file cells does mismatched"
#             assert np.all(
#                 self.seg_df.columns[3:] ==
#                 self.guide_df[self.GUIDE_SAMPLES_COLUMN]), \
#                 "guide file and seg file cells ordering mismatched"
#
#         if self.clone_df is not None:
#             assert len(self.sample_names) == len(self.clone_df), \
#                 "clone file size mismatched"
#
#         if self.tree_df is not None:
#             assert len(self.sample_names) == len(self.tree_df) + 1, \
#                 "tree file size mismatched"
#             self.tree_df = self.tree_df.ix[:, 0:4].copy()
#             self.data['tree'] = self.tree_df
#
#         if self.ratio_df is not None:
#             self.ratio_df = self.ratio_df.ix[:, seg_columns].copy()
#             self.data['ratio'] = self.ratio_df
#             assert np.all(
#                 self.ratio_df.columns[3:] ==
#                 self.seg_df.columns[3:]), \
#                 "ration file cell ordering mismatched"

'''
Created on Dec 2, 2016

@author: lubo
'''
import numpy as np
import pandas as pd
import os
import zipfile


def load_df(filename):
    df = pd.read_csv(filename, sep='\t')
    return df


class DataLoader(dict):
    TYPES = set(['ratio', 'pinmat', 'clone', 'tree', 'seg', 'pins', 'guide'])
    GUIDE_SAMPLES_COLUMN = 'seq.unit.id'

    @classmethod
    def _organize_filenames(cls, namelist):
        result = {}
        for filename in namelist:
            parts = filename.split('.')
            assert len(parts) > 2
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
            print(filenames)
            print(set(filenames.keys()))
            print(self.TYPES)
            assert set(filenames.keys()) == self.TYPES
            for filetype, filename in filenames.items():
                infile = zipdata.open(filename)
                df = pd.read_csv(infile, sep='\t')
                assert df is not None
                self[filetype] = df

    def _load_dir(self, dir_filename):
        assert os.path.exists(dir_filename)
        assert os.path.isdir(dir_filename)
        all_filenames = [
            os.path.join(dir_filename, f) for f in os.listdir(dir_filename)
            if os.path.isfile(os.path.join(dir_filename, f))]
        print(all_filenames)
        filenames = self._organize_filenames(all_filenames)
        print(filenames)
        print(set(filenames.keys()))
        print(self.TYPES)

        for filetype, filename in filenames.items():
            print("loading: {}".format(filename))
            infile = open(filename)
            df = pd.read_csv(infile, sep='\t')
            assert df is not None
            self[filetype] = df

    def __init__(self, filename):
        if os.path.isdir(filename):
            self._load_dir(filename)
        else:
            self._load_zipfile(filename)

        self.filename = filename

        self.seg_df = self['seg']
        self.ratio_df = self['ratio']
        self.clone_df = self['clone']
        self.tree_df = self['tree']
        self.guide_df = self['guide']
        self.pinmat_df = self['pinmat']
        self.pins_df = self['pins']
        self._filter_samples()

    def _filter_samples(self):
        self.sample_names = set(self.pinmat_df.columns)
        self.guide_df = self.guide_df[self.guide_df[
            self.GUIDE_SAMPLES_COLUMN].isin(self.sample_names)].copy()
        self.guide_df.reset_index(inplace=True)

        self['guide'] = self.guide_df

        assert len(self.sample_names) == len(self.guide_df)

        assert np.all(
            self.pinmat_df.columns ==
            self.guide_df[self.GUIDE_SAMPLES_COLUMN])
        assert len(self.sample_names) == len(self.clone_df)
        assert len(self.sample_names) == len(self.tree_df) + 1
        self.tree_df = self.tree_df.ix[:, 0:4].copy()
        self['tree'] = self.tree_df

        seg_columns = list(self.seg_df.columns[:3])
        for c in self.seg_df.columns[3:]:
            if c in self.sample_names:
                seg_columns.append(c)

        self.seg_df = self.seg_df.ix[:, seg_columns].copy()
        self['seg'] = self.seg_df
        assert np.all(
            self.seg_df.columns[3:] ==
            self.guide_df[self.GUIDE_SAMPLES_COLUMN])
        self.ratio_df = self.ratio_df.ix[:, seg_columns].copy()
        self['ratio'] = self.ratio_df
        assert np.all(
            self.ratio_df.columns[3:] ==
            self.guide_df[self.GUIDE_SAMPLES_COLUMN])

        assert len(self.seg_df.columns) == len(self.sample_names) + 3
        assert len(self.ratio_df.columns) == len(self.sample_names) + 3

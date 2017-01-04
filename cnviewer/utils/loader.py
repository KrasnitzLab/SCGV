'''
Created on Dec 2, 2016

@author: lubo
'''
import pandas as pd
import os
import zipfile


def load_df(filename):
    df = pd.read_csv(filename, sep='\t')
    return df


class DataLoader(dict):
    TYPES = set(['ratio', 'pinmat', 'clone', 'tree', 'seg', 'pins', 'guide'])
    GUIDE_SAMPLES_COLUMN = 'seq.unit.id'

    @staticmethod
    def _organize_filenames(namelist):
        result = {}
        for filename in namelist:
            parts = filename.split('.')
            assert len(parts) > 2
            filetype = parts[-2]
            result[filetype] = filename
        return result

    def __init__(self, zip_filename):
        assert os.path.isfile(zip_filename)
        assert os.path.exists(zip_filename)
        assert zipfile.is_zipfile(zip_filename)

        self.zip_filename = zip_filename
        with zipfile.ZipFile(self.zip_filename, 'r') as zipdata:
            filenames = self._organize_filenames(zipdata.namelist())
            assert set(filenames.keys()) == self.TYPES

            for filetype, filename in filenames.items():
                infile = zipdata.open(filename)
                df = pd.read_csv(infile, sep='\t')
                assert df is not None
                self[filetype] = df

        self.seg_df = self['seg']
        self.ratio_df = self['ratio']
        self.clone_df = self['clone']
        self.tree_df = self['tree']
        self.guide_df = self['guide']
        # print(self.guide_df['gate'].unique())
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
        self.ratio_df = self.ratio_df.ix[:, seg_columns].copy()
        self['ratio'] = self.ratio_df

        assert len(self.seg_df.columns) == len(self.sample_names) + 3
        assert len(self.ratio_df.columns) == len(self.sample_names) + 3

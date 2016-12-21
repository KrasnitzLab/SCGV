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
            print(zipdata.namelist())
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
        self.pinmat_df = self['pinmat']
        self.pins_df = self['pins']

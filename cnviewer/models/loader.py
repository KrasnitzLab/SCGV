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
    TYPES = set(['ratio', 'pinmat', 'clone', 'tree', 'seg', 'pins', 'guide'])
    GUIDE_SAMPLES_COLUMN = 'seq.unit.id'

    def __init__(self, filename):
        self.pathology = None
        self.data = {}
        self.filename = filename

    def load(self):
        if os.path.isdir(self.filename):
            self._load_dir(self.filename)
        else:
            self._load_zipfile(self.filename)

        self.seg_df = self.data.get('seg', None)
        self.ratio_df = self.data.get('ratio', None)
        self.clone_df = self.data.get('clone', None)
        self.tree_df = self.data.get('tree', None)
        self.guide_df = self.data.get('guide', None)
        self.pinmat_df = self.data.get('pinmat', None)
        self.pins_df = self.data.get('pins', None)

        assert self.seg_df is not None

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
            filename = os.path.join('pathology', row['image'])
            image = None
            if filename in zipdata.namelist():
                print("loading: ", filename)
                image = Image.open(zipdata.open(filename))
                # image.load()
            else:
                print("image not found: ", filename)
            filename = os.path.join('pathology', row['notes'])
            notes = None
            if filename in zipdata.namelist():
                print("loading: ", filename)
                notes = zipdata.open(filename).readlines()
                # image.load()
            else:
                print("image not found: ", filename)
            result[row['pathology']] = image, notes

        return result

    def _load_dir(self, dir_filename):
        assert os.path.exists(dir_filename)
        assert os.path.isdir(dir_filename)
        all_filenames = [
            os.path.join(dir_filename, f) for f in os.listdir(dir_filename)
            if os.path.isfile(os.path.join(dir_filename, f))]
        print(all_filenames)
        filenames = self._organize_filenames(all_filenames)

        for filetype, filename in filenames.items():
            print("loading: {}".format(filename))
            infile = open(filename)
            df = pd.read_csv(infile, sep='\t')
            assert df is not None
            self.data[filetype] = df

        self.pathology = None
        pathology_dirname = os.path.join(dir_filename, 'pathology')
        print('checking pahtology directory: {}'.format(pathology_dirname))
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
            filename = os.path.join(pathology_dirname, row['image'])
            print("looking for image in: {}".format(filename))
            image = None
            if os.path.exists(filename):
                image = Image.open(filename)
            filename = os.path.join(pathology_dirname, row['notes'])
            print("looking for notes in: {}".format(filename))
            notes = None
            if os.path.exists(filename):
                with open(filename, 'r') as notesfile:
                    notes = notesfile.readlines()
            result[row['pathology']] = image, notes
        return result

    def filter_samples(self):
        assert self.seg_df is not None

        if self.pinmat_df is None:
            return

        self.sample_names = set(self.pinmat_df.columns)
        seg_columns = list(self.seg_df.columns[:3])
        for c in self.seg_df.columns[3:]:
            if c in self.sample_names:
                seg_columns.append(c)

        self.seg_df = self.seg_df.ix[:, seg_columns].copy()
        self.data['seg'] = self.seg_df
        assert len(self.seg_df.columns) == len(self.sample_names) + 3

        if self.guide_df is not None:
            self.guide_df = self.guide_df[self.guide_df[
                self.GUIDE_SAMPLES_COLUMN].isin(self.sample_names)].copy()
            self.guide_df.reset_index(inplace=True)
            self.data['guide'] = self.guide_df

            assert len(self.sample_names) == len(self.guide_df)

            assert np.all(
                self.pinmat_df.columns ==
                self.guide_df[self.GUIDE_SAMPLES_COLUMN])
            assert np.all(
                self.seg_df.columns[3:] ==
                self.guide_df[self.GUIDE_SAMPLES_COLUMN])

        if self.clone_df is not None:
            assert len(self.sample_names) == len(self.clone_df)

        if self.tree_df is not None:
            assert len(self.sample_names) == len(self.tree_df) + 1
            self.tree_df = self.tree_df.ix[:, 0:4].copy()
            self.data['tree'] = self.tree_df

        if self.ratio_df is not None:
            self.ratio_df = self.ratio_df.ix[:, seg_columns].copy()
            self.data['ratio'] = self.ratio_df
            assert np.all(
                self.ratio_df.columns[3:] ==
                self.seg_df.columns[3:])

            assert len(self.ratio_df.columns) == len(self.sample_names) + 3

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


class DataLoader(dict):
    TYPES = set(['ratio', 'pinmat', 'clone', 'tree', 'seg', 'pins', 'guide'])
    GUIDE_SAMPLES_COLUMN = 'seq.unit.id'

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
            assert set(filenames.keys()) == self.TYPES
            for filetype, filename in filenames.items():
                infile = zipdata.open(filename)
                df = pd.read_csv(infile, sep='\t')
                assert df is not None
                self[filetype] = df
            self.pathology = self._load_images_zipfile(zipdata)

    def _load_images_zipfile(self, zipdata):
        descriptor = 'pathology/description.csv'
        if descriptor not in zipdata.namelist():
            return
        infile = zipdata.open(descriptor)
        images_df = pd.read_csv(infile)

        result = {}
        for _index, row in images_df.iterrows():
            filename = os.path.join('images', row['image'])
            image = None
            if filename in zipdata.namelist():
                print("loading: ", filename)
                image = Image.open(zipdata.open(filename))
                # image.load()
            else:
                print("image not found: ", filename)
            filename = os.path.join('images', row['notes'])
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
        print(filenames)
        print(set(filenames.keys()))
        print(self.TYPES)

        for filetype, filename in filenames.items():
            print("loading: {}".format(filename))
            infile = open(filename)
            df = pd.read_csv(infile, sep='\t')
            assert df is not None
            self[filetype] = df

        self.pathology = None
        images_dirname = os.path.join(dir_filename, 'pathology')
        if os.path.exists(images_dirname) and os.path.isdir(images_dirname):
            self.pathology = self._load_images_dir(images_dirname)

    def _load_images_dir(self, images_dirname):
        filename = os.path.join(images_dirname, 'description.csv')
        images_df = pd.read_csv(filename)
        result = {}
        for _index, row in images_df.iterrows():
            filename = os.path.join(images_dirname, row['image'])
            print("looking for image in: {}".format(filename))
            image = None
            if os.path.exists(filename):
                image = Image.open(filename)
            filename = os.path.join(images_dirname, row['notes'])
            print("looking for notes in: {}".format(filename))
            notes = None
            if os.path.exists(filename):
                with open(filename, 'r') as notesfile:
                    notes = notesfile.readlines()
            result[row['pathology']] = image, notes
        return result

    def __init__(self, filename):
        self.pathology = None

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

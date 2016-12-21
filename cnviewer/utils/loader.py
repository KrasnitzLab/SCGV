'''
Created on Dec 2, 2016

@author: lubo
'''
import pandas as pd


def load_df(filename):
    df = pd.read_csv(filename, sep='\t')
    return df


class DataLoader(object):

    def __init__(self, zip_filename):
        self.zip_filename = zip_filename

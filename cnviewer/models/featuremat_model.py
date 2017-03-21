'''
Created on Feb 28, 2017

@author: lubo
'''
from models.model_delegate import ModelDelegate


class FeaturematModel(ModelDelegate):

    def __init__(self, model):
        super(FeaturematModel, self).__init__(model)
        assert self.model.data.features_df is not None
        assert self.model.data.featuremat_df is not None
        self.heatmap = self.model.make_featuremat(ordering=self.ordering) + 2.0

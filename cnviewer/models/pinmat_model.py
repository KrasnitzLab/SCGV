'''
Created on Feb 28, 2017

@author: lubo
'''
from models.model_delegate import ModelDelegate


class PinmatModel(ModelDelegate):

    def __init__(self, model):
        super(PinmatModel, self).__init__(model)
        assert self.model.data.pins_df is not None
        assert self.model.data.pinmat_df is not None
        self.heatmap = self.model.pinmat + 2.0

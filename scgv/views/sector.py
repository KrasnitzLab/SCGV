'''
Created on Dec 15, 2016

@author: lubo
'''
from scgv.views.track import TrackViewer


class SectorViewer(TrackViewer):

    def __init__(self, model):
        super(SectorViewer, self).__init__(
            model, "Sectors", model.sector, model.sector_mapping)

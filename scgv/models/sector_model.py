'''
Created on Jan 10, 2017

@author: lubo
'''
import numpy as np
from scgv.models.model import BaseModel, DataModel


class SectorsDataModel(BaseModel):

    def __init__(self, model):
        super(SectorsDataModel, self).__init__(model.data)
        self.model = model
        assert self.model.sector is not None

    def make_ordering(self):
        index = np.array(self.model.Z['leaves'])
        order = np.arange(len(index))

        sector = self.model.sector
        self.sector_mapping = self.model.sector_mapping

        res = np.lexsort(
            (
                order,
                sector,
            ))

        return index[res]


class TrackDataModel(BaseModel):

    def __init__(self, model, track_index):
        super(TrackDataModel, self).__init__(model.data)
        self.model = model
        assert self.model.tracks is not None
        assert track_index < len(self.model.tracks) and track_index >= 0

        self.tracks = self.model.tracks
        self.track_index, self.track_name, self.track, self.track_mapping = \
            self.model.tracks[track_index]
        assert self.track_index == track_index

    def make_ordering(self):
        index = np.array(self.model.Z['leaves'])
        order = np.arange(len(index))

        track = self.track

        res = np.lexsort(
            (
                order,
                track,
            ))

        return index[res]


class SingleSectorDataModel(BaseModel):

    def __init__(self, model, sector_id):
        super(SingleSectorDataModel, self).__init__(model.data)
        if isinstance(model, DataModel):
            self.model = model
        else:
            self.model = model.model
        assert self.model.sector is not None
        assert self.model.sector_mapping is not None

        self.sector_mapping = self.model.sector_mapping
        self.sector_id = None

        if sector_id in self.sector_mapping:
            self.sector_id = sector_id
        else:
            for key, value in self.sector_mapping.items():
                if sector_id == value:
                    self.sector_id = key

        assert self.sector_id in self.sector_mapping

        self.bins, self.samples = self.model.seg_data.shape
        self.lmat = None

    def make_ordering(self):
        index = np.array(self.model.Z['leaves'])
        order = np.arange(len(index))

        sector = self.model.sector

        res = np.lexsort(
            (
                order,
                sector,
            ))

        return index[res]

    def make_subtree(self):

        return self.get_subtree(
            self.model.lmat[:],
            self.model._original_column_labels(),
            self.column_labels
        )

    @staticmethod
    def remove_leaf(lmat, leafNames, removeName):
        ans = dict()
        ans["lmat"] = []
        ans["leafNames"] = []

        # find number of leaf to remove
        newLeafNames = []
        removeNumber = -1
        for i in range(len(leafNames)):
            if leafNames[i] == removeName:
                removeNumber = i
            else:
                newLeafNames.append(leafNames[i])

        if removeNumber == -1:
            return ans

        # remove row from lmat
        newLmat = []
        parentNumber = -1
        partnerNumber = -1
        for i in range(len(lmat)):
            if lmat[i][0] == removeNumber:
                parentNumber = len(leafNames) + i
                partnerNumber = lmat[i][1]
            elif lmat[i][1] == removeNumber:
                parentNumber = len(leafNames) + i
                partnerNumber = lmat[i][0]
            else:
                newLmat.append(list(lmat[i]))

        if parentNumber == -1:
            print("ERROR PARENT NUMBER")
            return ans

        # update parent row
        for i in range(len(newLmat)):
            if newLmat[i][0] == parentNumber:
                newLmat[i][0] = partnerNumber
                newLmat[i][3] -= 1
                break
            if newLmat[i][1] == parentNumber:
                newLmat[i][1] = partnerNumber
                newLmat[i][3] -= 1
                break

        # decrement all numbers > parentNumber and then > removeNumber
        for i in range(len(newLmat)):
            if newLmat[i][0] > parentNumber:
                newLmat[i][0] -= 1
            if newLmat[i][1] > parentNumber:
                newLmat[i][1] -= 1

        for i in range(len(newLmat)):
            if newLmat[i][0] > removeNumber:
                newLmat[i][0] -= 1
            if newLmat[i][1] > removeNumber:
                newLmat[i][1] -= 1

        ans["lmat"] = newLmat
        ans["leafNames"] = newLeafNames
        return ans

    @classmethod
    def get_subtree(cls, lmat, fulltreeLeafNames, subtreeLeafNames):
        removeList = []

        for i in range(len(fulltreeLeafNames)):
            if fulltreeLeafNames[i] in subtreeLeafNames:
                pass
            else:
                removeList.append(fulltreeLeafNames[i])

        workLeafNames = list(fulltreeLeafNames)
        workLmat = []
        for i in range(len(lmat)):
            workLmat.append(list(lmat[i]))

        for i in range(len(removeList)):
            rlans = cls.remove_leaf(workLmat, workLeafNames, removeList[i])
            workLmat = rlans["lmat"]
            workLeafNames = rlans["leafNames"]
        return workLmat

    def make(self):
        self.ordering = self.make_ordering()
        self.sector, self.sector_mapping = \
            self.make_sector(ordering=self.ordering)

        sector_val = self.sector_mapping[self.sector_id]
        sector_index = self.sector == sector_val
        print(sector_val, sector_index)

        self.column_labels = self.make_column_labels(ordering=self.ordering)
        self.column_labels = self.column_labels[sector_index]

        self.lmat = self.make_subtree()
        self.Z = self.make_dendrogram(self.lmat)

        self.samples = len(self.column_labels)
        self.interval_length = self.make_interval_length(self.Z)
        self.label_midpoints = self.make_label_midpoints()

        self.bins = self.model.bins

        self.clone, self.subclone = self.make_clone(
            ordering=self.ordering)
        if self.clone is not None:
            self.clone = self.clone[sector_index]
            self.subclone = self.subclone[sector_index]

        self.heatmap = self.make_heatmap(
            ordering=self.ordering)
        self.heatmap = self.heatmap[:, sector_index]

        # self.gate = self.model.make_gate(
        #     ordering=self.ordering)
        # if self.gate is not None:
        #     self.gate = self.gate[sector_index]

        if self.sector is not None:
            self.sector = self.sector[sector_index]

        self.multiplier = self.model.make_multiplier(
            ordering=self.ordering)
        if self.multiplier is not None:
            self.multiplier = self.multiplier[sector_index]

        self.error = self.model.make_error(
            ordering=self.ordering)
        if self.error is not None:
            self.error = self.error[sector_index]


def remove_leaf(lmat, leafNames, removeName):
    ans = dict()
    ans["lmat"] = []
    ans["leafNames"] = []

    # find number of leaf to remove
    newLeafNames = []
    removeNumber = -1
    for i in range(len(leafNames)):
        if leafNames[i] == removeName:
            removeNumber = i
        else:
            newLeafNames.append(leafNames[i])

    if removeNumber == -1:
        return ans

    # remove row from lmat
    newLmat = []
    parentNumber = -1
    partnerNumber = -1
    for i in range(len(lmat)):
        if lmat[i][0] == removeNumber:
            parentNumber = len(leafNames) + i
            partnerNumber = lmat[i][1]
        elif lmat[i][1] == removeNumber:
            parentNumber = len(leafNames) + i
            partnerNumber = lmat[i][0]
        else:
            newLmat.append(list(lmat[i]))

    if parentNumber == -1:
        print("ERROR PARENT NUMBER")
        return ans

    # update parent row
    for i in range(len(newLmat)):
        if newLmat[i][0] == parentNumber:
            newLmat[i][0] = partnerNumber
            newLmat[i][3] -= 1
            break
        if newLmat[i][1] == parentNumber:
            newLmat[i][1] = partnerNumber
            newLmat[i][3] -= 1
            break

    # decrement all numbers > parentNumber and then > removeNumber
    for i in range(len(newLmat)):
        if newLmat[i][0] > parentNumber:
            newLmat[i][0] -= 1
        if newLmat[i][1] > parentNumber:
            newLmat[i][1] -= 1

    for i in range(len(newLmat)):
        if newLmat[i][0] > removeNumber:
            newLmat[i][0] -= 1
        if newLmat[i][1] > removeNumber:
            newLmat[i][1] -= 1

    ans["lmat"] = newLmat
    ans["leafNames"] = newLeafNames
    return ans


def get_subtree(lmat, fulltreeLeafNames, subtreeLeafNames):
    removeList = []

    for i in range(len(fulltreeLeafNames)):
        if fulltreeLeafNames[i] in subtreeLeafNames:
            pass
        else:
            removeList.append(fulltreeLeafNames[i])

    workLeafNames = list(fulltreeLeafNames)
    workLmat = []
    for i in range(len(lmat)):
        workLmat.append(list(lmat[i]))

    for i in range(len(removeList)):
        rlans = remove_leaf(workLmat, workLeafNames, removeList[i])
        workLmat = rlans["lmat"]
        workLeafNames = rlans["leafNames"]
    return workLmat


class SingleTrackDataModel(BaseModel):

    def __init__(self, model, track_index, track_value):
        super(SingleTrackDataModel, self).__init__(model.data)
        if isinstance(model, DataModel):
            self.model = model
        else:
            self.model = model.model
        assert self.model.tracks is not None
        assert track_index < len(self.model.tracks) and track_index >= 0

        self.tracks = self.model.tracks
        self.track_index, self.track_name, self.track, self.track_mapping = \
            self.model.tracks[track_index]
        assert self.track_index == track_index

        self.track_value_key = None
        for key, value in self.track_mapping.items():
            if track_value == value:
                self.track_value_key = key

        assert self.track_value_key in self.track_mapping, \
            [self.track_value_key, self.track_mapping]

        self.bins, self.samples = self.model.seg_data.shape
        self.lmat = None

    def make_ordering(self):
        index = np.array(self.model.Z['leaves'])
        order = np.arange(len(index))

        track = self.track

        res = np.lexsort(
            (
                order,
                track,
            ))

        return index[res]

    def make_subtree(self):

        return get_subtree(
            self.model.lmat[:],
            self.model._original_column_labels(),
            self.column_labels
        )

    def make(self):
        self.ordering = self.make_ordering()
        self.track, self.track_mapping = \
            self.make_track(self.track_name, ordering=self.ordering)

        track_val = self.track_mapping[self.track_value_key]
        track_index = self.track == track_val
        print(track_val, track_index)

        self.column_labels = self.make_column_labels(ordering=self.ordering)
        self.column_labels = self.column_labels[track_index]

        self.lmat = self.make_subtree()
        self.Z = self.make_dendrogram(self.lmat)

        self.samples = len(self.column_labels)
        self.interval_length = self.make_interval_length(self.Z)
        self.label_midpoints = self.make_label_midpoints()

        self.bins = self.model.bins

        self.clone, self.subclone = self.make_clone(
            ordering=self.ordering)
        if self.clone is not None:
            self.clone = self.clone[track_index]
            self.subclone = self.subclone[track_index]

        self.heatmap = self.make_heatmap(
            ordering=self.ordering)
        self.heatmap = self.heatmap[:, track_index]

        # self.gate = self.model.make_gate(
        #     ordering=self.ordering)
        # if self.gate is not None:
        #     self.gate = self.gate[sector_index]

        # if self.sector is not None:
        #     self.sector = self.sector[track_index]
        self.sector = None

        self.multiplier = self.model.make_multiplier(
            ordering=self.ordering)
        if self.multiplier is not None:
            self.multiplier = self.multiplier[track_index]

        self.error = self.model.make_error(
            ordering=self.ordering)
        if self.error is not None:
            self.error = self.error[track_index]

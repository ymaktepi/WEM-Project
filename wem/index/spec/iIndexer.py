from abc import ABCMeta, abstractclassmethod


class iIndexer(metaclass=ABCMeta):
    def __init__(self):
        self._index = None

    @abstractclassmethod
    def getIndex(self):
        return self._index

    @abstractclassmethod
    def saveIndex(self):
        pass

    @abstractclassmethod
    def restoreIndex(self):
        pass

    @abstractclassmethod
    def createIndex(self, documentGenerator):
        pass

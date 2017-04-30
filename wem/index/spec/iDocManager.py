from abc import ABCMeta, abstractclassmethod


class iDocManager(metaclass=ABCMeta):

    @abstractclassmethod
    def saveToPickle(self, Document):
        pass

    @abstractclassmethod
    def openPickle(self, Document):
        pass

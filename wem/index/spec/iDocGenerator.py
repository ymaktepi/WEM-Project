from abc import ABCMeta, abstractclassmethod


class iDocGenerator(metaclass=ABCMeta):
    """
    Generate documents
    """

    def __init__(self):
        pass

    @abstractclassmethod
    def createDocumentTuple(self):
        """
        Yield list of documents
        """
        pass

    @abstractclassmethod
    def getDocumentTuple(self):
        """
        Return a list of Documents
        """
        pass

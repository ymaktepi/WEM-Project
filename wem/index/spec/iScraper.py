from abc import ABCMeta, abstractclassmethod


class iScraper(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractclassmethod
    def getUrlList(self):
        """
        List of URL
        :return: 
        """
        pass

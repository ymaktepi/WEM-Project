from wem.index.ctftimeScraper import ctftimeScraper
from wem.index.ctftimeDocManager import ctftimeDocManager
from wem.index.ctftimeDocGenerator import ctftimeDocGenerator

if __name__ == '__main__':

    # Create url list
    scrapper = ctftimeScraper().createUrlList()

    # Create documents
    #gen = ctftimeDocGenerator(scrapper).createDocumentTuple()

    # Save documents in pickle
    #docManager = ctftimeDocManager().saveToPickle(gen.getDocumentTuple())

    # Get list of documents
    #docManager.getDocuments()



from wem.index.ctftimeScraper import ctftimeScraper
from wem.index.ctftimeDocManager import ctftimeDocManager
from wem.index.ctftimeDocGenerator import ctftimeDocGenerator

if __name__ == '__main__':

    # Create url list
    #scrapper = ctftimeScraper().createUrlList()

    scrapper = ctftimeScraper().openPickle('./save/ctftime_urls_1493571830.p')

    mofos = ['https://ctftime.org/writeup/6632', 'https://ctftime.org/writeup/6631']
    # Create documents
    gen = ctftimeDocGenerator(scrapper)
    gen.createDocumentTuple(mofos)

    # Save documents in pickle
    docManager = ctftimeDocManager().saveToPickle(gen.getDocumentTuple())

    # Get list of documents
    docManager = ctftimeDocManager()
    docManager.openPickle('./save/'+docManager.getFileName())

    #print(file)



from wem.index.ctftimeScraper import ctftimeScraper
from wem.index.ctftimeDocManager import ctftimeDocManager
from wem.index.ctftimeDocGenerator import ctftimeDocGenerator
from wem.index.ctftimeIndexer import ctftimeIndexer
import requests, time
from multiprocessing import Pool

def para_docs(doc):
    url = 'https://ctftime.org/writeup/' + str(doc.getId())

    #print(doc.getId())

    if (doc.getMeta()['url'] != url):
        text = doc.getContentRaw()
        doc.setMeta(gen.getWriteupMeta(text, doc.getMeta()))

    return doc

if __name__ == '__main__':

    # ------------------------------------------------
    # PARSE CTFTIME AND SAVE IN A PICKLE
    # ------------------------------------------------

    # Create url list
    #scrapper = ctftimeScraper().createUrlList()

    #scrapper = ctftimeScraper()
    #scrapper.openPickle('./save/ctftime_urls_1493571830.p')

    # Create documents
    #gen = ctftimeDocGenerator(scrapper)
    #gen.createDocumentTuple()

    # Save documents in pickle
    #docManager = ctftimeDocManager().saveToPickle(gen.getDocumentTuple())

    # ------------------------------------------------
    # META COMPLETION
    # ------------------------------------------------

    #scrapper = ctftimeScraper()
    #scrapper.openPickle('./save/ctftime_urls_1493571830.p')

    # Get list of documents
    #docManager = ctftimeDocManager()
    #documents = docManager.openPickle('./save/ctftime_docs_1493937491.p')

    #gen = ctftimeDocGenerator(scrapper)

    #p = Pool(30)
    #total = p.map(para_docs, documents)

    #print(len(total))
    #ctftimeDocManager().saveToPickle(total)

    # ------------------------------------------------
    # INDEX
    # ------------------------------------------------

    scrapper = ctftimeScraper()
    scrapper.openPickle('./save/ctftime_urls_1493571830.p')

    # Get list of documents
    docManager = ctftimeDocManager()
    documents = docManager.openPickle('./save/ctftime_docs_1493991150.p')

    print(len(documents))

    indexer = ctftimeIndexer()
    indexer.createSchema()
    indexer.createIndex(documents)

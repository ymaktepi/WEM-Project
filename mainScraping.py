from wem.index.ctftimeScraper import ctftimeScraper
from wem.index.ctftimeDocManager import ctftimeDocManager
from wem.index.ctftimeDocGenerator import ctftimeDocGenerator
from wem.index.ctftimeIndexer import ctftimeIndexer
from wem.index.quouairiManadgeure import QueryManager

def main():
    settings = {
        'get_url_web': False,
        'scraping_web': False,
        'index_web': True,

        'file_urls':'./save/ctftime_urls_1493571830.p',
        'file_docs': './save/ctftime_docs_1493991150.p'
    }

    scrapper = ctftimeScraper()
    docManager = ctftimeDocManager()
    indexer = ctftimeIndexer()


    # --------------------------------------------------------------------------
    # URL LIST
    # --------------------------------------------------------------------------
    if settings['get_url_web']:

        # Create url list
        url_file = scrapper.createUrlList()
        print("Saved url list into: %s" % url_file)
    else:
        scrapper.openPickle(settings['file_urls'])


    # --------------------------------------------------------------------------
    # WEB SCRAPER
    # --------------------------------------------------------------------------
    doc_file = None
    if settings['scraping_web']:

        # Create documents
        gen = ctftimeDocGenerator(scrapper)
        gen.createDocumentTuple()

        # Save documents in pickle
        doc_file = docManager.saveToPickle(gen.getDocumentTuple())
    else:
        doc_file = docManager.openPickle(settings['file_docs'])

    # --------------------------------------------------------------------------
    # INDEXER
    # --------------------------------------------------------------------------
    if settings['index_web']:


        # Create Schema and create index
        indexer.createSchema()
        indexer.createIndex(doc_file)

        # Save in indexdir directory
        indexer.saveIndex()
    else:
        # Load indexed documents
        indexer.restoreIndex()

    with QueryManager(indexer.getIndex()) as qm:
        for result in qm.textQuouairiz("javascript"):
            print(result.__dict__["rank"])


if __name__ == '__main__':
    main()

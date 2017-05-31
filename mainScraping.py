from wem.index.ctftimeScraper import ctftimeScraper
from wem.index.ctftimeDocManager import ctftimeDocManager
from wem.index.ctftimeDocGenerator import ctftimeDocGenerator
from wem.index.ctftimeIndexer import ctftimeIndexer
from wem.index.quouairiManadgeure import QueryManager
from wem.index.toolsIndexer import toolsIndexer
from wem.index.settings import Settings

def main():

    scrapper = ctftimeScraper(Settings._FILE_URLS)
    docManager = ctftimeDocManager(Settings._FILE_DOCS)
    indexer = ctftimeIndexer()
    toolIndex = toolsIndexer()


    # --------------------------------------------------------------------------
    # URL LIST
    # --------------------------------------------------------------------------

    if Settings._GET_URL_WEB:

        # Create url list
        url_file = scrapper.createUrlList()
        print("Saved url list into: %s" % url_file)
    else:
        scrapper.openPickle(Settings._FILE_URLS)


    # --------------------------------------------------------------------------
    # WEB SCRAPER
    # --------------------------------------------------------------------------

    if Settings._SCRAPING_WEB:

        # Create documents
        gen = ctftimeDocGenerator(scrapper)
        gen.createDocumentTuple()

        # Save documents in pickle
        doc_file = docManager.saveToPickle(gen.getDocumentTuple())
    else:
        doc_file = docManager.openPickle(Settings._FILE_DOCS)

    # --------------------------------------------------------------------------
    # INDEXER
    # --------------------------------------------------------------------------

    if Settings._INDEX_WEB:

        # Create Schema and create index
        indexer.createSchema()
        indexer.createIndex(doc_file)

        # Save in indexdir directory
        indexer.saveIndex()
    else:
        # Load indexed documents
        indexer.restoreIndex()

    with QueryManager(indexer.getIndex(), 'text') as qm:
        for result in qm.text_query("javascript"):
            print(result)

    # --------------------------------------------------------------------------
    # TOOL INDEXER
    # --------------------------------------------------------------------------

    if Settings._INDEX_TOOL:

        # Create Schema and create index
        toolIndex.createSchema()
        toolIndex.createIndex(None)

        # Save in indexdir directory
        toolIndex.saveIndex()
    else:
        # Load indexed documents
        toolIndex.restoreIndex()

    with QueryManager(toolIndex.getIndex(), 'description') as qm:
        for result in qm.text_query("tcpdump"):
            print(result['title'])

    return indexer, toolIndex


if __name__ == '__main__':
    main()

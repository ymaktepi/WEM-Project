from wem.index.ctftimeScraper import ctftimeScraper
from wem.index.ctftimeDocManager import ctftimeDocManager
from wem.index.ctftimeDocGenerator import ctftimeDocGenerator
from wem.index.ctftimeIndexer import ctftimeIndexer
from wem.index.toolsIndexer import toolsIndexer

def loadScraper():
    settings = {
        'get_url_web': False,
        'scraping_web': False,
        'index_web': False,
        'index_tool': False,

        'file_urls': '/save/ctftime_urls_1493571830.p',
        'file_docs': '/save/ctftime_docs_1493991150.p',
        'dict_tools': '/dict/tools.csv',

        'root': ''
    }

    scrapper = ctftimeScraper(settings['file_urls'])
    docManager = ctftimeDocManager(settings['file_docs'])
    indexer = ctftimeIndexer(settings['root'])
    toolIndex = toolsIndexer(settings['root'], settings['dict_tools'])

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

    # --------------------------------------------------------------------------
    # TOOL INDEXER
    # --------------------------------------------------------------------------

    if settings['index_tool']:

        # Create Schema and create index
        toolIndex.createSchema()
        toolIndex.createIndex(None)

        # Save in indexdir directory
        toolIndex.saveIndex()
    else:
        # Load indexed documents
        toolIndex.restoreIndex()

    return indexer, toolIndex
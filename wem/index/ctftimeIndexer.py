from wem.index.spec.iIndexer import iIndexer
from bs4 import BeautifulSoup

from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.analysis import LowercaseFilter, StopFilter, CharsetFilter, StandardAnalyzer

import os, os.path
from whoosh import index
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser
from whoosh.support.charset import accent_map


class ctftimeIndexer(iIndexer):
    def __init__(self):
        super().__init__()

        self._analyser = StandardAnalyzer() | LowercaseFilter() | StopFilter() | CharsetFilter(accent_map)

        self._schema = Schema(id=ID(stored=True, unique=True),
                              text=TEXT(analyzer=self._analyser, stored=True),
                              title=TEXT(stored=True),
                              author=TEXT,
                              tags=KEYWORD(lowercase=True, scorable=True),
                              event=TEXT,
                              url=TEXT,

                              tag_title=TEXT,

                              meta_title=TEXT,
                              meta_description=TEXT,
                              meta_keywords=KEYWORD(lowercase=True, scorable=True),
                              meta_og_title=TEXT,
                              meta_og_description=TEXT,
                              meta_twitter_title=TEXT,
                              meta_twitter_description=TEXT
                              )
        self._index = None
        self._indexFolderName = "indexdir"
        self._documentList = []

    def createIndex(self, documentList):

        writer = AsyncWriter(self._index)

        for doc in documentList:

            text = ' '.join(self.getContent(doc.getContentRaw()))

            metas = doc.getMeta()
            writer.add_document (
                text = text,
                title = metas['title'],
                author = metas['author'],
                tags = metas['tag'],
                event = metas['event'],
                url = metas['url'],

                tag_title = metas['tag_title'] if 'tag_title' in metas else '',

                meta_title = metas['meta_title'] if 'meta_title' in metas else '',
                meta_description = metas['meta_description'] if 'meta_description' in metas else '',
                meta_keywords = metas['meta_keywords'] if 'meta_keywords' in metas else '',
                meta_og_title = metas['meta_og:title'] if 'meta_og:title' in metas else '',
                meta_og_description = metas['meta_og:description'] if 'meta_og:description' in metas else '',
                meta_twitter_title = metas['meta_twitter:title'] if 'meta_twitter:title' in metas else '',
                meta_twitter_description = metas['meta_twitter:description'] if 'meta_twitter:description' in metas else ''
            )

        writer.commit(optimize=True)



        with self._index.searcher() as searcher:
            numdocs = searcher.doc_count()
            print(numdocs)

            results = searcher.document(tags="sqli")
            print(results)

        ix = open_dir(self._indexFolderName)
        with ix.searcher() as searcher:
            query = QueryParser("text", ix.schema).parse(u'begin')
            results = searcher.search(query)
            print(results)
            for result in results:
                print(result)


    def getIndex(self):
        pass

    def saveIndex(self):
        pass

    def restoreIndex(self):
        pass

    def createSchema(self):
        if not os.path.exists(self._indexFolderName):
            os.mkdir(self._indexFolderName)

        self._index = create_in(self._indexFolderName, self._schema)

    def visible(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

    def getContent(self, text):
        data = BeautifulSoup(text, 'html.parser').findAll(text=True)

        result = list(filter(self.visible, data))

        removeItems = ['<link rel=', '<script src=', '<link href=']
        result = [i.strip().lower().replace("\n", " ") for i in result]
        result = [i for i in result if (not i.startswith(tuple(removeItems)) and len(i) > 3)]

        return result

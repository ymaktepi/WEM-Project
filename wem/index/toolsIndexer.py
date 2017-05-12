from wem.index.spec.iIndexer import iIndexer

from whoosh import index
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.writing import AsyncWriter
from whoosh.support.charset import accent_map
from whoosh.analysis import LowercaseFilter, StopFilter, CharsetFilter, StandardAnalyzer

import os, os.path, csv

class toolsIndexer(iIndexer):
    def __init__(self, root, filename):
        super().__init__()


        self._index = None
        self._indexFolderName = root + "/toolindexdir"
        self._documentList = []
        self._analyser = StandardAnalyzer() | LowercaseFilter() | StopFilter() | CharsetFilter(accent_map)
        self._schema = Schema(id=ID(stored=True, unique=True),
                              category=TEXT(stored=True),
                              title=TEXT(stored=True),
                              url=TEXT(stored=True),
                              description=TEXT(analyzer=self._analyser, stored=True)
                              )
        self._filename = filename

    def createIndex(self, documentList):

        self._writer = AsyncWriter(self._index)

        with open(self._filename, newline='') as csvfile:
            docs = csv.reader(csvfile, delimiter=';')
            for doc in docs:
                self._writer.add_document(
                    title=doc[1],
                    category=doc[0],
                    url=doc[2],
                    description=doc[3]
                )


    def getIndex(self):
        return self._index

    def saveIndex(self):
        self._writer.commit(optimize=True)

    def restoreIndex(self):
        self._index = index.open_dir(self._indexFolderName)

    def createSchema(self):
        if not os.path.exists(self._indexFolderName):
            os.mkdir(self._indexFolderName)

        self._index = create_in(self._indexFolderName, self._schema)


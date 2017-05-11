from whoosh.qparser import QueryParser


class QueryManager(object):

    def __init__(self, index):
        """
        Creates a query manager
        :param index: a WHOOOOOSH index
        """
        self._index = index
        self._queryParser = QueryParser("text", schema=self._index.schema)

    def __enter__(self):
        self._searcher = self._index.searcher()
        return self

    def __exit__(self, type, value, traceback):
        self._searcher.close()

    def textQuouairiz(self, text):
        quouairy = self._queryParser.parse(text)
        results = self._searcher.search(quouairy)
        return results
        '''with self._index.searcher() as searcher:
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
                print(result)'''

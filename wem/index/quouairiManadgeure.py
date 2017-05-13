from whoosh import scoring
from whoosh.qparser import MultifieldParser


class QueryManager(object):
    def __init__(self, index, fieldList):
        """
        Creates a query manager
        :param index: a WHOOOOOSH index
        """
        self._index = index
        self._queryParser = MultifieldParser(fieldList, schema=self._index.schema)

    def __enter__(self):
        self._searcher = self._index.searcher(weighting=scoring.TF_IDF())
        return self

    def __exit__(self, type, value, traceback):
        self._searcher.close()

    def textQuouairiz(self, text):
        quouairy = self._queryParser.parse(text)
        results = self._searcher.search(quouairy)
        return results

from whoosh import scoring
from whoosh.qparser import MultifieldParser
from whoosh.query import And, Or, Term

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

    def textQuouairiz(self, text, category_field="", category=[], language_field="", language=[]):
        query = self._queryParser.parse(text)
        # return self._searcher.search(query, limit=50)
        terms = None
        categories = None
        languages = None

        if len(category) > 0:
            categories = And([Term(category_field, cat) for cat in category])
            terms = categories

        if len(language) > 0:
            languages = And([Term(language_field, lang) for lang in language])
            terms = languages

        if len(category) > 0 and len(language) > 0:
            terms = And([categories, languages])

        if terms is not None:
            return self._searcher.search(query, limit=50, filter=terms)
        else:
            return self._searcher.search(query, limit=50)

import sys
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

    def text_query(self, text, metadata, page):
        query_text = None
        if text != "":
            query_text = self._queryParser.parse(text)
            
        # Construct the filter terms object
        terms = None
        terms_list = []
        for field, values in metadata.items():
            if len(values) > 0:
                terms_list.append(And([Term(field, value) for value in values]))
        if len(terms_list) > 0:
            terms = And(terms_list)

        print(query_text)
        print(terms)

        # Make the query with (i) just words, or (ii) both (iii) or just terms
        if query_text is not None and terms is not None:
            query = And([query_text, terms])
        elif query_text is not None:
            query = query_text
        elif terms is not None:
            query = terms
        else:
            raise Exception('No input provided!')

        return self._searcher.search_page(query, page, pagelen=20)
        # return self._searcher.search(query, limit=50)

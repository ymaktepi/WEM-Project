class Document(object):
    def __init__(self, id, content, meta):
        self._id = id
        self._content = content
        self._meta = meta

    def getId(self):
        return self._id

    def getContent(self):
        return self._content

    def getMeta(self):
        return self._meta

class Document(object):
    def __init__(self, id, content, meta):
        self._id = id
        self._content_raw = content
        self._meta = meta
        self._content_parsed = []

    def getId(self):
        return self._id

    def getContentRaw(self):
        return self._content_raw

    def getMeta(self):
        return self._meta

    def setMeta(self, value):
        self._meta = value

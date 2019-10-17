"""Map of short links to the full urls."""
from google.cloud import firestore

LINKS_COLLECTION_NAME = u'links'
URL_KEY = u'url'

class Links:

    def __init__(self):
        self.db = firestore.Client()
        self.links = self.db.collection(LINKS_COLLECTION_NAME)

    def has(self, keyword):
        doc_ref = self.links.document(keyword)
        doc = doc_ref.get()
        return doc.exists

    def insert(self, keyword, url):
        doc_ref = self.links.document(keyword)
        data = {URL_KEY: url}
        doc_ref.set(data)

    def get(self, keyword):
        if not self.has(keyword):
            return None

        doc_ref = self.links.document(keyword)
        doc = doc_ref.get()
        doc_dict = doc.to_dict()
        url = doc_dict[URL_KEY]

        return url


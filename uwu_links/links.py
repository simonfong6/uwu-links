"""Map of short links to the full urls."""
from google.cloud import firestore
from google.cloud.firestore import Increment

LINKS_COLLECTION_NAME = u'links'
TOTAL_VISITS_COLLECTION_NAME = u'total_visits'
URL_KEY = u'url'
VISIT_COUNT_KEY = u'visit_count'
COUNT_KEY = u'count'

class Links:

    def __init__(self):
        self.db = firestore.Client()
        self.links = self.db.collection(LINKS_COLLECTION_NAME)
        self.total_visits = self.db.collection(TOTAL_VISITS_COLLECTION_NAME).document('visits')

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

        self.increment(keyword)

        return url

    def increment(self, keyword):
        doc_ref = self.links.document(keyword)
        doc_ref.update({VISIT_COUNT_KEY: Increment(1)})
        self.increment_total_visits()

    def increment_total_visits(self):
        total_visits = self.total_visits.get()
        if not total_visits.exists:
            self.total_visits.set({COUNT_KEY: 0})
        self.total_visits.update({COUNT_KEY: Increment(1)})

    def get_all_links(self):
        """Fetch all links from database."""
        link_dicts = []

        links = self.links.stream()

        for link in links:
            link_dict = link.to_dict()
            link_dict['key'] = link.id
            link_dicts.append(link_dict)

        return link_dicts

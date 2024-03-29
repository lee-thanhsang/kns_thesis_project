from utils.querier.query_builder import *
from utils.es_client.es_client import *


class Searcher:
    def __init__(self):
        self.__es_client = EsClient()

    def search(self, query):
        print(query)
        es_res = self.__es_client.search('thesis', query)
        activities = []
        for item in es_res['hits']['hits']:
            activities.append(item)

        return activities

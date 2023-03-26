from elasticsearch import Elasticsearch


class EsClient:
    def __init__(self):
        self.__client = Elasticsearch('http://localhost:9200')

    def create_index(self, index_name):
        self.__client.indices.create(
            index=index_name, settings={
                'index': {
                    'similarity': {
                        'default_similarity': {
                            'type': 'BM25',
                            'k1': 1.2,
                            'b': 0.75
                        }
                    },
                    'max_ngram_diff': 3,
                },

                'analysis': {
                    'filter': {
                        'whitespace_remove': {
                            'type': 'pattern_replace',
                            'pattern': ' ',
                            'replacement': ''
                        },
                        '2_5_grams': {
                            'type': 'edge_ngram',
                            'min_gram': 2,
                            'max_gram': 15,
                        }
                    },
                    'analyzer': {
                        'rebuilt_whitespace': {
                            'tokenizer': 'whitespace',
                            'filter': [
                                'lowercase',
                                'asciifolding'
                            ]
                        },
                        'concatenate_whitespace': {
                            'tokenizer': 'standard',
                            'filter': [
                                'lowercase',
                                'asciifolding',
                                'whitespace_remove',
                                '2_5_grams'
                            ]
                        },
                        'ngram_splitter': {
                            'tokenizer': 'split_ngram_tokenizer',
                            'filter': [
                                'lowercase',
                                'asciifolding'
                            ]
                        }
                    },

                    'tokenizer': {
                        'split_ngram_tokenizer': {
                            'type': 'ngram',
                            'min_gram': 2,
                            'max_gram': 3,
                            'token_chars': [
                                'letter', 'digit', 'punctuation',
                            ]
                        }
                    }
                }
            }, mappings={
                'properties': {
                    'name': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'name:alt': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'contact': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'host': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'job_description': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'number': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'requirement': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'place': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'time:start': {
                        'type': 'text',
                        'analyzer': 'concatenate_whitespace',
                        'similarity': 'default_similarity',
                    },
                    'time:end': {
                        'type': 'text',
                        'analyzer': 'concatenate_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'benefit:drl': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },
                    'benefit:ctxh': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },
                    'benefit:others': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },

                    'register:way': {
                        'type': 'text',
                        'analyzer': 'rebuilt_whitespace',
                        'similarity': 'default_similarity',
                    },
                    'register:time:start': {
                        'type': 'text',
                        'analyzer': 'concatenate_whitespace',
                        'similarity': 'default_similarity',
                    },
                    'register:time:end': {
                        'type': 'text',
                        'analyzer': 'concatenate_whitespace',
                        'similarity': 'default_similarity',
                    },
                },
            }
        )

    def insert_one(self, index_name, id, data):
        self.__client.create(index=index_name, id=id, document=data)

    def search(self, index_name, query):
        return self.__client.search(index=index_name, query=query)
    
    def count(self, index_name, query):
        return self.__client.count(index=index_name, query=query)
    
    
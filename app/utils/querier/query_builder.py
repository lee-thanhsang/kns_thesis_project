import math
import copy

MATCH_RATE = 5/6

initial_query = {
    'bool': {
        'must': [],
        'must_not': [],
        'filter': [],
        'should': [],
    }
}


class QueryBuilder:
    def __init__(self):
        self.__query = copy.deepcopy(initial_query)

    def add(self, cond_type, match_type, field, value):
        if field != 'name':
            self.__query['bool'][cond_type].append({
                match_type: {
                    field: value,
                }
            })

            return

        self.__query['bool'][cond_type].append({
            match_type: {
                field: {
                    'query': value,
                    'minimum_should_match': math.ceil(len(value.split())*MATCH_RATE),
                    'fuzziness': 1,
                },
            }
        })

    def get_query(self):
        return self.__query

    def reset_query(self):
        self.__query = initial_query

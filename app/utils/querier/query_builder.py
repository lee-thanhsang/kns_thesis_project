import math
import copy

MATCH_RATE = 1/2

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
        if field == 'name':
            self.__query['bool'][cond_type].append({
                match_type: {
                    field: {
                        'query': value,
                        # 'minimum_should_match': math.ceil(len(value.split())*MATCH_RATE),
                        # 'fuzziness': 0,
                    },
                }
            })

        elif field in ['benefit:drl', 'benefit:ctxh']:
            compare = {
                'gte': value[0]
            }
            if len(value) > 1:
                compare['lte'] = value[1]

            self.__query['bool'][cond_type].append({
                match_type: {
                    field: compare,
                }
            })

        elif field in ['time:start', 'time:end', 'register:time:start', 'register:time:end']:
            if value[0] == value[1]:
                self.__query['bool'][cond_type].append({
                    match_type: {
                        field: {
                            'gte': value[0],
                            'lte': value[1],
                        }
                    }
                })
            else:
                self.__query['bool'][cond_type].append({
                    match_type: {
                        field: {
                            'gte': value[0],
                            'lt': value[1],
                        }
                    }
                })
        
        else:
            self.__query['bool'][cond_type].append({
                match_type: {
                    field: value,
                }
            })

    def get_query(self):
        return self.__query

    def reset_query(self):
        self.__query = initial_query

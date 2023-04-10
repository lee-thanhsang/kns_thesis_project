from collections import defaultdict
import copy
import app.utils.querier.searcher as searcher
import app.utils.querier.query_builder as query_builder


no_query_keys = ['number', 'register:way', 'job_description']

SCORE_RATE = 0.9


class Querier:
    searcher = searcher.Searcher()

    def __init__(self):
        self.cached_db_slot = defaultdict(dict)
        self.cached_db = defaultdict(dict)
        self.no_query = no_query_keys
        # Querier.searcher = searcher.Searcher()
        # self.match_key = usersim_default_key

    def fill_inform_slot(self, inform_slot_to_fill, current_inform_slots):
        """
        Given the current informs/constraints fill the informs that need to be filled with values from the database.

        Searches through the database to fill the inform slots with PLACEHOLDER with values that work given the current
        constraints of the current episode.

        Parameters:
            inform_slot_to_fill (dict): Inform slots to fill with values
            current_inform_slots (dict): Current inform slots with values from the StateTracker

        Returns:
            dict: inform_slot_to_fill filled with values
        """

        # For this simple system only one inform slot should ever passed in
        assert len(inform_slot_to_fill) == 1

        key = list(inform_slot_to_fill.keys())[0]

        # This removes the inform we want to fill from the current informs if it is present in the current informs
        # so it can be re-queried
        current_informs = copy.deepcopy(current_inform_slots)
        current_informs.pop(key, None)

        # db_results is a dict of dict in the same exact format as the db, it is just a subset of the db
        db_results = self.get_db_results(current_informs)
        filled_inform = {}
        if len(db_results) == 0:
            filled_inform[key] = 'no match available'
        else:
            highest_score = db_results[list(db_results.keys())[0]]['_score']
            i = 0
            value = None
            while i < len(db_results) and not value and db_results[list(db_results.keys())[i]]['_score'] >= highest_score * SCORE_RATE:
                value = db_results[list(db_results.keys())[i]]['_source'].get(key)
                i =+ 1

            if not value:
                value = 'no match available'

            if not isinstance(value, str):
                filled_inform[key] = max(value, key=len)
            else:
                filled_inform[key] = value
        # filled_inform = {}
        # values_dict = self._count_slot_values(key, db_results)
        # if len(db_results) > 1:
        #     filled_inform[key] = 'no match available'
        # else:
        # if values_dict:
        #     # Get key with max value (ie slot value with highest count of available results)
        #     filled_inform[key] = max(values_dict, key=values_dict.get)
        # else:

        return filled_inform

    def _count_slot_values(self, key, db_subdict):
        """
        Return a dict of the different values and occurrences of each, given a key, from a sub-dict of database

        Parameters:
            key (string): The key to be counted
            db_subdict (dict): A sub-dict of the database

        Returns:
            dict: The values and their occurrences given the key
        """

        slot_values = defaultdict(int)  # init to 0
        for id in db_subdict.keys():
            current_option_dict = db_subdict[id]
            # If there is a match
            if key in current_option_dict.keys():
                slot_value = current_option_dict[key]
                # This will add 1 to 0 if this is the first time this value has been encountered, or it will add 1
                # to whatever was already in there
                slot_values[slot_value] += 1
        return slot_values

    def get_db_results(self, constraints):
        """
        Get all items in the database that fit the current constraints.

        Looks at each item in the database and if its slots contain all constraints and their values match then the item
        is added to the return dict.

        Parameters:
            constraints (dict): The current informs

        Returns:
            dict: The available items in the database
        """
        # Filter non-queryable items and keys with the value 'anything' since those are inconsequential to the constraints
        new_constraints = {k: v for k, v in constraints.items(
        ) if k not in self.no_query and v != 'anything' and v != 'no match available'}

        inform_items = frozenset(new_constraints.items())
        # print('Constraints Search')
        # print(inform_items)
        # print(self.cached_db)
        cache_return = self.cached_db[inform_items]

        if cache_return == None:
            # If it is none then no matches fit with the constraints so return an empty dict
            return {}
        # if it isnt empty then return what it is
        if cache_return:
            return cache_return
        # else continue on
        # print('constraints search')
        # print(new_constraints)

        available_options = {}
        query = query_builder.QueryBuilder()
        for k, v in new_constraints.items():
            # self.query_builder.add('must', 'match', k, v.replace('_', ' '))
            query.add('must', 'match', k, v.replace('_', ' '))

        # activities = Querier.searcher.search(self.query_builder.get_query())
        activities = Querier.searcher.search(query.get_query())
        for item in activities:
            self.cached_db[inform_items].update(
                {item['_id']: item})
            available_options.update(
                {item['_id']: item})
        #     print(activity_map[item['_id']])
        # raise
        # for id in self.database.keys():
        #     current_option_dict = self.database[id]
        #     # First check if that database item actually contains the inform keys
        #     # Note: this assumes that if a constraint is not found in the db item then that item is not a match
        #     if len(set(new_constraints.keys()) - set(self.database[id].keys())) == 0:
        #         match = True
        #         # Now check all the constraint values against the db values and if there is a mismatch don't store
        #         for k, v in new_constraints.items():
        #             # if fuzz.ratio(str(v).lower(), str(current_option_dict[k]).lower()) < 50:
        #             if str(v).lower() != str(current_option_dict[k]).lower():
        #                 match = False
        #             # else:
        #             #     print(str(v).lower())
        #             #     print(str(current_option_dict[k]).lower())
        #             #     print("Score: {}".format(fuzz.ratio(str(v).lower(), str(current_option_dict[k]).lower())))
        #         if match:
        #             # Update cache
        #             self.cached_db[inform_items].update({id: current_option_dict})
        #             available_options.update({id: current_option_dict})

        # if nothing available then set the set of constraint items to none in cache
        if not available_options:
            self.cached_db[inform_items] = None

        return available_options

    def get_db_results_for_slots(self, current_informs):
        """
        Counts occurrences of each current inform slot (key and value) in the database items.

        For each item in the database and each current inform slot if that slot is in the database item (matches key
        and value) then increment the count for that key by 1.

        Parameters:
            current_informs (dict): The current informs/constraints

        Returns:
            dict: Each key in current_informs with the count of the number of matches for that key
        """

        # The items (key, value) of the current informs are used as a key to the cached_db_slot
        inform_items = frozenset(current_informs.items())
        # A dict of the inform keys and their counts as stored (or not stored) in the cached_db_slot
        cache_return = self.cached_db_slot[inform_items]

        if cache_return:
            return cache_return

        # If it made it down here then a new query was made and it must add it to cached_db_slot and return it
        # Init all key values with 0
        db_results = {key: 0 for key in current_informs.keys()}
        db_results['matching_all_constraints'] = 0

        # searcher = ActivitiesSearcher()
        # searcher.search_activities('query', 'match_all', )
        # res = self.es_client.search('thesis', query={'match_all': {}})
        # print(self.es_client.count_document('thesis', query={'match_all': {}}))
        query = query_builder.QueryBuilder()
        for CI_key, CI_value in current_informs.items():
            if CI_key in self.no_query:
                continue
            if CI_value == 'anything':
                db_results[CI_key] = int(
                    len(Querier.searcher.search(query.get_query())))
            else:
                local_query = query_builder.QueryBuilder()
                local_query.add(
                    'must', 'match', CI_key, CI_value.replace('_', ' '))
                query.add(
                    'must', 'match', CI_key, CI_value.replace('_', ' '))
                db_results[CI_key] = int(
                    len(Querier.searcher.search(local_query.get_query())))

        # Get all documents match all constraints
        db_results['matching_all_constraints'] = int(
            len(Querier.searcher.search(query.get_query())))

        # for id in self.database.keys():
        #     all_slots_match = True
        #     for CI_key, CI_value in current_informs.items():
        #         # Skip if a no query item and all_slots_match stays true
        #         if CI_key in self.no_query:
        #             continue
        #         # If anything all_slots_match stays true AND the specific key slot gets a +1
        #         if CI_value == 'anything':
        #             db_results[CI_key] += 1
        #             continue
        #         if CI_key in self.database[id].keys():

        #             if fuzz.ratio(CI_value.lower(), self.database[id][CI_key].lower()) > 90:
        #                 # print('Get DB for result')
        #                 # print(CI_value.lower())
        #                 # print(self.database[id][CI_key].lower())
        #                 # print(fuzz.ratio(CI_value.lower(), self.database[id][CI_key].lower()))
        #             # if CI_value.lower() == self.database[id][CI_key].lower():
        #                 db_results[CI_key] += 1
        #             else:
        #                 all_slots_match = False
        #         else:
        #             all_slots_match = False
        #     if all_slots_match: db_results['matching_all_constraints'] += 1

        # update cache (set the empty dict)
        self.cached_db_slot[inform_items].update(db_results)
        assert self.cached_db_slot[inform_items] == db_results
        return db_results

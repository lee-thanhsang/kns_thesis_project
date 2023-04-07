import random
from utils.querier.searcher import *
from utils.querier.query_builder import *
from fuzzywuzzy import fuzz
import string
import json


INFORMS = ['place', 'host', 'time:start', 'time:end',
           'benefit:ctxh', 'benefit:drl', 'benefit:others', 'job_description']
INFORMS_RATE_FOR_CHOOSING = [0.8, 0.8, 0.4, 0.4, 0.6, 0.6, 0.3, 0.3]
SCORE_RATE = 0.5
FIELD_NAME_MIN_SCORE = 0.8
OTHER_FIELD_MIN_SCORE = 0.7
IN_FIELD_MIN_MATCH_RATE = 0.6
MIN_NEARLY_EQUAL_FIELDS = 2
MIN_REMOVE_WORDS = 5
MAX_REMOVE_WORDS = 10
MAX_REPLACE_WORDS = 3
MAX_REMOVE_CHARACTERS_PER_WORD = 3


# inform_map = {
#     'name': ['name'],
#     'place': ['place'],
#     'host': ['host'],
#     'time': ['time:start', 'time:end'],
#     'benefit': ['benefit:ctxh', 'benefit:drl', 'benefit:others'],
#     'job_description': ['job_description'],
# }

class Querier:
    def __init__(self):
        self.__searcher = Searcher()

    def create_inform_list(self, num_of_informs):
        inform_list = []
        inform_list.append('name')
        remaining_informs = copy.deepcopy(INFORMS)
        remaining_inform_rate = copy.deepcopy(INFORMS_RATE_FOR_CHOOSING)

        for _ in range(num_of_informs - 1):
            inform = random.choices(
                remaining_informs, weights=remaining_inform_rate)[0]
            inform_list.append(inform)
            idx = remaining_informs.index(inform)
            remaining_informs.pop(idx)
            remaining_inform_rate.pop(idx)

        return inform_list

    def get_inform_slot(self, inform, activities):
        inform_slots = []
        search_scores = []
        for activity in activities:
            if inform in activity['_source'].keys():
                inform_slots.append(activities['_source'][inform])
                search_scores.append(activity['_score'])

        if len(inform_slots) == 0:
            return None

        return random.choices(inform_slots, weights=search_scores)[0]

    # def search_by_informs(self, informs, activities):
    #     query = QueryBuilder()
    #     for inform in informs:
    #         inform_slot = self.get_inform_slot(inform, activities)
    #         if inform_slot:
    #             query.add('must', 'match', inform, inform_slot)

    #     activities = self.__searcher.search(query.get_query())
    #     return activities

    def filter_by_score(self, activities):
        activities = sorted(activities, key=lambda x: x['_score'])
        activities.reverse()
        if not activities or len(activities) == 0:
            return []

        highest_score = activities[0]['_score']
        filtered_activities = []
        for activity in activities:
            if activity['_score'] >= highest_score * SCORE_RATE:
                filtered_activities.append(activity)

        return filtered_activities

    def compare_activities(self, first_activity, second_acitivity):
        if fuzz.token_set_ratio(first_activity['_source']['name'], second_acitivity['_source']['name']) < FIELD_NAME_MIN_SCORE:
            return False

        nearly_equal_fields = 0
        for k in first_activity['_source'].keys():
            if k == 'name':
                continue

            if k not in second_acitivity['_source'].keys():
                continue

            min_field_match = 1
            if isinstance(first_activity['_source'][k], list):
                min_field_match = min(len(first_activity['_source'][k]), len(
                    second_acitivity['_source'][k]))

            field_match = 0
            for first_element in first_activity['_source'][k]:
                for second_element in second_acitivity['_source'][k]:
                    if fuzz.token_set_ratio(first_element, second_element) > OTHER_FIELD_MIN_SCORE:
                        field_match += 1
                        break

            # print(field_match, min_field_match)
            if field_match >= min_field_match * IN_FIELD_MIN_MATCH_RATE:
                nearly_equal_fields += 1

        if nearly_equal_fields >= MIN_NEARLY_EQUAL_FIELDS:
            return True

        return False


class TextReformer:
    def remove_words(self, text):
        remove_words = random.randint(MIN_REMOVE_WORDS, MAX_REMOVE_WORDS)
        if isinstance(text, list):
            text = random.choice(text)

        words = text.split()
        if int(len(words) / 2) < remove_words:
            remove_words = int(len(words) / 2)

        remove_positions = random.sample(range(0, len(words)), remove_words)
        remove_positions.sort(reverse=True)
        for position in remove_positions:
            words.pop(position)

        return ' '.join(words)

    def replace_characters_in_words(self, text):
        replace_words = random.randint(0, MAX_REPLACE_WORDS)
        if isinstance(text, list):
            text = random.choice(text)

        words = text.split()
        if int(len(words) / 2) < replace_words:
            replace_words = int(len(words) / 2)

        random_positions = random.sample(range(0, len(words)), replace_words)
        # print('words: ', words, 'random_positions ', random_positions)
        for position in random_positions:
            word = words[position]
            replace_characters = random.randint(
                0, MAX_REMOVE_CHARACTERS_PER_WORD)
            if replace_characters > int(len(word) / 2):
                replace_characters = int(len(word) / 2)

            # print(words, position, word, replace_characters)
            replace_positions = random.sample(
                range(0, len(word)), replace_characters)
            for pos in replace_positions:
                word_list = list(word)
                word_list[pos] = random.choice(string.ascii_lowercase)
                word = ''.join(word_list)

            words[position] = word

        return ' '.join(words)

    def get_benefit_drl_or_ctxh(self, benefit_list):
        if len(benefit_list) == 0:
            return

        if len(benefit_list) == 1:
            return [random.uniform(0, benefit_list[0])]

        if len(benefit_list) > 1:
            return [random.uniform(min(benefit_list), max(benefit_list))]

        return

    def get_time(self, time):
        dmy_time = time.split()[-1]
        dmy_time_parts = dmy_time.split('-')

        is_remove = random.randint(0, 1)
        if is_remove == 1 and len(dmy_time_parts) > 1:
            dmy_time_parts.pop(0)

        start_time = '-'.join(dmy_time_parts)
        dmy_time_parts[0] = str(int(dmy_time_parts[0]) + 1)
        if int(dmy_time_parts[0]) > 12 and len(dmy_time_parts) == 2:
            dmy_time_parts[0] = '01'
            dmy_time_parts[1] = str(int(dmy_time_parts[1]) + 1)

        if int(dmy_time_parts[0]) > 30 and len(dmy_time_parts) == 3:
            dmy_time_parts[0] = '01'
            dmy_time_parts[1] = str(int(dmy_time_parts[1]) + 1)
            if int(dmy_time_parts[1]) > 12:
                dmy_time_parts[1] = '01'
                dmy_time_parts[2] = str(int(dmy_time_parts[2]) + 1)

        if len(dmy_time_parts[0]) == 1:
            dmy_time_parts[0] = '0' + dmy_time_parts[0]

        if len(dmy_time_parts) > 1 and len(dmy_time_parts[1]) == 1:
            dmy_time_parts[1] = '0' + dmy_time_parts[1]

        end_time = '-'.join(dmy_time_parts)

        return [start_time, end_time]


class QueryBenchmark:
    def __init__(self):
        self.__querier = Querier()
        self.__text_reformer = TextReformer()
        self.__searcher = Searcher()
        self.__activities = []
        with open('benchmark_tool/data/normalize_activity.json') as file:
            activities = json.load(file)
            for activity in activities:
                self.__activities.append(activity['activity'])

    def run_benchmark(self, num_of_informs, keep_activity=False):
        inform_list = self.__querier.create_inform_list(num_of_informs)

        satisfied_activities = copy.deepcopy(self.__activities)
        query = QueryBuilder()
        inform_history = {}
        print(inform_list)
        activity = random.choice(satisfied_activities)
        print(activity)
        for (i, inform) in enumerate(inform_list):
            if len(satisfied_activities) == 0:
                continue

            if not keep_activity:
                activity = random.choice(satisfied_activities)

            if inform not in activity:
                continue

            text = activity[inform]
            if inform in ['name', 'place', 'host', 'benefit:others']:
                text = self.__text_reformer.remove_words(text)
                text = self.__text_reformer.replace_characters_in_words(text)
                query.add('must', 'match', inform, text)

            elif inform in ['benefit:ctxh', 'benefit:drl']:
                text = self.__text_reformer.get_benefit_drl_or_ctxh(text)
                query.add('must', 'range', inform, text)

            elif inform in ['time:start', 'time:end']:
                text = self.__text_reformer.get_time(text)
                query.add('must', 'range', inform, text)

            inform_history[inform] = text
            res = self.__searcher.search(query.get_query())
            satisfied_activities = []
            for item in res:
                satisfied_activities.append(item['_source'])

            print('INFORM:', inform)
            print('TEXT:', text)
            print('LENGTH:', len(satisfied_activities))

            filter_score_activities = self.__querier.filter_by_score(
                copy.deepcopy(res))
            print('FILTER_SCORE_LENGTH:', len(filter_score_activities))

            compare_activity_map = {}
            for i, item in enumerate(filter_score_activities):
                activity_clone = copy.deepcopy(item)
                for k in compare_activity_map.keys():
                    if not self.__querier.compare_activities(compare_activity_map[k], activity_clone):
                        continue

                compare_activity_map[i] = item

            compare_activities = list(compare_activity_map)
            print('COMPARE_ACTIVITY_LENGTH:', len(compare_activities))

        # print('activity', activity)

        print('result: ', satisfied_activities[0] if len(
            satisfied_activities) > 0 else None)
        # for item in satisfied_activities:
        #     print(item)

from fuzzywuzzy import fuzz
import copy

SCORE_RATE = 0.5
FIELD_NAME_MIN_SCORE = 0.8
OTHER_FIELD_MIN_SCORE = 0.7
IN_FIELD_MIN_MATCH_RATE = 0.6
MIN_NEARLY_EQUAL_FIELDS = 2


class ActivityFilter:
    def filter_and_compare(self, activities):
        filter_score_activities = self.__querier.filter_by_score(copy.deepcopy(activities))
        compare_activity_map = {}
        for i, item in enumerate(filter_score_activities):
            activity_clone = copy.deepcopy(item)
            for k in compare_activity_map.keys():
                if not self.__querier.compare_activities(compare_activity_map[k], activity_clone):
                    continue

            compare_activity_map[i] = item

        compare_activities = list(compare_activity_map)
        return compare_activities

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

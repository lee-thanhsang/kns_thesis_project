# import pattern_responce_sentence as pattern_responce_sentence
import services.pattern_responce_sentence as pattern_responce_sentence
import random
from utils.state_tracker.state_tracker import StateTracker
from utils.state_tracker.intent_slot_state import *
from utils.cookie.cookie_generator import *
from utils.parser.parser import *
import pickle
import threading

SLOT_SEPARATOR = ', '

class V2ResponseSentenceService:
    def __init__(
        self,
        intent_slot_svc_cli,
        action_decider_svc_cli,
        redis,
        clickhouse_cli,
    ):
        self.__intent_slot_svc_cli = intent_slot_svc_cli
        self.__action_decider_svc_cli = action_decider_svc_cli
        self.__redis = redis
        self.__clickhouse_client = clickhouse_cli
        self.__slot_intent_state_context = IntentSlotStateContext()
        self.__time_parser = TimeParser()
        self.__benefit_parser = BenefitParser()

    def get_intent_and_slot_from_sentence(self, message, user_id, log):
        state_tracker = StateTracker()
        is_cache = False
        if user_id:
            state_tracker_str = self.__redis.get_value_from_key('states:' + user_id + ':state_tracker')
            db_helper_str = self.__redis.get_value_from_key('states:' + user_id + ':db_helper')
            if state_tracker_str and db_helper_str:
                is_cache = True
                state_tracker = pickle.loads(state_tracker_str)
                db_helper = pickle.loads(db_helper_str)
                state_tracker.db_helper = db_helper
            else:
                user_id = generate_cookie()
        else:
            user_id = generate_cookie()

        # Log user_id and is_cache here.
        log['user_id'] = str(user_id)
        log['is_cache'] = is_cache

        # Log raw request here.
        log['raw_request'] = str(message)

        intent, slot = self.__intent_slot_svc_cli.get_intent_and_slot(message)
        reformed_slot = self.reform_slot_value(slot)
        inform_slots = reformed_slot
        
        # Log intent, slot and reformed slot here.
        log['intent'] = str(intent)
        log['slot'] = str(slot)
        log['reformed_slot'] = str(reformed_slot)

        if intent in reformed_slot.keys():
            log['confirmation'] = str((intent, reformed_slot[intent]))
        
        request_slots = {}
        if intent not in ['inform', 'greeting', 'complete', 'meaningless', 'activities', 'anything']:
            if intent == 'jobdescription':
                intent = 'job_description'

            if intent == 'registerway':
                intent = 'register:way'
            
            if intent == 'registerdate':
                intent = 'register:time'

            request_slots = {intent: 'UNK'}
            intent = 'request'
        
        if intent == 'anything':
            intent = 'inform'

        self.__slot_intent_state_context.set_state_object(
            'user', intent, request_slots, inform_slots)
        state_tracker = self.__slot_intent_state_context.update_state_tracker(
            state_tracker)
        
        # If intent is greeting or complete, just return responce
        if intent in ['greeting', 'complete', 'meaningless', 'UNK']:
            self.cache_current_state(user_id, state_tracker, log)
            return {'intent': intent, 'request_slots': {}, 'inform_slots': {}}, user_id
        
        if intent in ['activities']:
            activities = state_tracker.get_activities()
            state_tracker.reset()
            self.cache_current_state(user_id, state_tracker, log)
            return {'intent': 'activities', 'value': activities}, user_id
        
        if not state_tracker.get_first_user_request():
            self.cache_current_state(user_id, state_tracker, log)
            return 'Bọn mình đã lưu thông tin hoạt động. Bạn muốn hỏi điều gì về hoạt động.', user_id
        
        state = state_tracker.get_state()

        # Log state which is generated from tracker here.
        log['state'] = str(state)

        if state is None:
            state_tracker.reset()
            self.cache_current_state(user_id, state_tracker, log)
            return {'intent': 'no_document', 'request_slots': {}, 'inform_slots': {}}, user_id
        
        if state_tracker.round_num > state_tracker.max_round_num:
            state_tracker.reset()
            self.cache_current_state(user_id, state_tracker, log)
            return 'Vượt quá số lần hỏi về hoạt động.', user_id
        
        if state_tracker.get_first_user_request() and request_slots and len(request_slots) > 0:
            if list(state_tracker.get_first_user_request().keys())[0] != list(request_slots.keys())[0]:
                return 'Bạn không thể hỏi khi câu hỏi trước chưa được trả lời.', user_id

        action = self.__action_decider_svc_cli.get_action(state)
        
        # Log action here.
        log['action'] = str(action)

        intent = action['intent']
        request_slots = action['request_slots']
        inform_slots = action['inform_slots']

        print(state_tracker.user_requests)
        if intent == 'inform' and len(state_tracker.user_requests) > 0 and list(state_tracker.user_requests[0].keys())[0] not in inform_slots.keys():
            log['wrong_decision'] = str({
                'user_request': state_tracker.user_requests[0],
                'agent_inform': inform_slots,
            })

        self.__slot_intent_state_context.set_state_object(
            'agent', intent, request_slots, inform_slots)
        state_tracker = self.__slot_intent_state_context.update_state_tracker(
            state_tracker)
        

        if intent in ['done', 'thank']:
            self.cache_current_state(user_id, state_tracker, log)
            return {'intent': intent, 'request_slots': {}, 'inform_slots': {}}, user_id

        answer = state_tracker.get_answer()
        if answer:
            print('answer ', answer)
            state_tracker.reset_answer()
            state_tracker.remove_user_requests(
                list(state_tracker.get_first_user_request().keys())[0])
            # if state_tracker.get_first_user_request() is None:
            #     state_tracker.reset()

        question = state_tracker.get_cur_action()
        if question:
            print('question ', question)

        state_tracker.reform_current_informs()
        self.cache_current_state(user_id, state_tracker, log)

        return answer if answer else question, user_id

    def make_response_sentence(self, data):
        if isinstance(data, str):
            return '' + data
        
        if isinstance(data, list):
            return str(data)
        
        raw_intent = data.get('intent', False)
        
        if raw_intent in ['request', 'inform']:
            intent = None
            value = None
            if raw_intent == 'request':
                request_slots = list(data.get('request_slots', False).items())[0]
                intent = request_slots[0] + '_' + raw_intent
                
                sentence = self.get_pattern_responce_sentence(intent)
                return sentence

            if raw_intent == 'inform':
                inform_slots = list(data.get('inform_slots', False).items())[0]
                intent = inform_slots[0].replace(':', '_')
                value = inform_slots[1]

                if value == "not match available":
                    return "Thông tin này hiện chưa được cập nhật."

                val_in_msg = ''
                if value:
                    sentence = self.get_pattern_responce_sentence(intent)

                    val_in_msg = ', '.join(value) if isinstance(value, list) else value
                    return sentence.replace('KEYWORD', val_in_msg)
                else:
                    "Thông tin này hiện chưa được cập nhật."
            

        elif raw_intent in ['complete', 'thanks', 'done']:
            sentence = self.get_pattern_responce_sentence('complete')
            return sentence
        
        elif raw_intent == 'greeting':
            sentence = self.get_pattern_responce_sentence('greeting')
            return sentence
        
        elif raw_intent in ['meaningless', 'UNK']:
            sentence = self.get_pattern_responce_sentence('meaningless')
            return sentence
        
        #[FUTURE_FIX] Add pattern and replace this case.
        elif raw_intent == 'no_document':
            return 'Rất tiếc, không tìm thấy hoạt động nào dựa trên yêu cầu của bạn.'
        
        #[FUTURE_FIX] Add pattern for responsing all activities.
        elif raw_intent == 'activities':
            activities = data.get('value', False)
            
            if activities:
                activities_lst = '\n- '.join([activity['_source']['name'] for activity in activities])
                return 'Một số hoạt động phù hợp với yêu cầu của bạn là:\n- ' + activities_lst
            else:
                return "Rất tiếc, không tìm thấy hoạt động nào dựa trên yêu cầu của bạn."
            
    def end_dialog(self, user_id):
        self.__redis.remove_by_key('states:' + user_id + ':state_tracker')
        self.__redis.remove_by_key('states:' + user_id + ':db_helper')
        return

    def get_pattern_responce_sentence(self, intent):
        return random.sample(getattr(pattern_responce_sentence, intent), 1)[0]

    def cache_current_state(self, user_id, state_tracker, log):
        # Log current informs and history of state tracker here.
        log['current_informs'] = str(state_tracker.current_informs)
        log['history'] = str(state_tracker.history)

        # thread = threading.Thread(target=self.__clickhouse_client.create_dialog, kwargs={'log': log})
        # thread.start()
        self.__redis.set_key_value('states:' + user_id + ':db_helper', pickle.dumps(state_tracker.db_helper))
        delattr(state_tracker, 'db_helper')
        self.__redis.set_key_value('states:' + user_id + ':state_tracker', pickle.dumps(state_tracker))

    def reform_slot_value(self, slot):
        reformed_slot = {}
        for key in slot.keys():
            if key in ['time:start', 'time:end', 'register:time:start', 'register:time:end']:
                sub_slots = slot[key].split(SLOT_SEPARATOR)
                time_ranges = []
                for sub_slot in sub_slots:
                    time_range = self.__time_parser.parse(sub_slot)
                    if time_range is not None:
                        time_ranges.append(time_range)

                if len(time_ranges) == 1:
                    reformed_slot[key] = [self.__time_parser.to_string(time_ranges[0][0]), self.__time_parser.to_string(time_ranges[0][1])]
                elif len(time_ranges) > 1:
                    time_ranges = sorted(time_ranges)
                    reformed_slot[key] = [self.__time_parser.to_string(time_ranges[0][0]), self.__time_parser.to_string(time_ranges[-1][0])]

            elif key in ['benefit:drl', 'benefit:ctxh']:
                sub_slots = slot[key].split(SLOT_SEPARATOR)
                benefits = []
                for sub_slot in sub_slots:
                    sub_slot_benefits = self.__benefit_parser.parse(sub_slot)
                    for item in sub_slot_benefits:
                        benefits.append(item)

                if len(benefits) == 1:
                    reformed_slot[key] = [benefits[0]]
                elif len(benefits) > 1:
                    reformed_slot[key] = [min(benefits), max(benefits)]

            elif key in ['jobdescription']:
                reformed_slot['job_description'] = slot[key].replace('_', ' ')

            else:
                reformed_slot[key] = slot[key].replace('_', ' ')

        return reformed_slot

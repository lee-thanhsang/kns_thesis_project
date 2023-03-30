# import pattern_responce_sentence as pattern_responce_sentence
import app.services.pattern_responce_sentence as pattern_responce_sentence
import random
from app.utils.state_tracker.state_tracker import StateTracker
from app.utils.state_tracker.intent_slot_state import *
from app.utils.cookie.cookie_generator import *
import pickle


class V2ResponseSentenceService:
    def __init__(
        self,
        intent_slot_svc_cli,
        action_decider_svc_cli,
        redis,
    ):
        self.__intent_slot_svc_cli = intent_slot_svc_cli
        self.__action_decider_svc_cli = action_decider_svc_cli
        self.__redis = redis
        self.__slot_intent_state_context = IntentSlotStateContext()

    def get_intent_and_slot_from_sentence(self, message, user_id):
        state_tracker = StateTracker()
        if user_id:
            state_tracker_str = self.__redis.get_value_from_key(user_id + ':state_tracker')
            db_helper_str = self.__redis.get_value_from_key(user_id + ':db_helper')
            if state_tracker_str and db_helper_str:
                state_tracker = pickle.loads(state_tracker_str)
                db_helper = pickle.loads(db_helper_str)
                state_tracker.db_helper = db_helper
            else:
                user_id = generate_cookie()
        else:
            user_id = generate_cookie()
        
        intent, slot = self.__intent_slot_svc_cli.get_intent_and_slot(message)
        print(intent, slot)

        # If intent is greeting or complete, just return responce
        if intent in ['greeting', 'complete']:
            return {'intent': intent, 'request_slots': {}, 'inform_slots': {}}, user_id
        
        inform_slots = slot
        request_slots = {}
        if intent not in ['inform', 'greeting', 'complete', 'meaningless']:
            request_slots = {intent: 'UNK'}
            intent = 'request'

        self.__slot_intent_state_context.set_state_object(
            'user', intent, request_slots, inform_slots)
        state_tracker = self.__slot_intent_state_context.update_state_tracker(
            state_tracker)

        state = state_tracker.get_state()
        action = self.__action_decider_svc_cli.get_action(state)
        print(vars(state_tracker))

        intent = action['intent']
        request_slots = action['request_slots']
        inform_slots = action['inform_slots']
        self.__slot_intent_state_context.set_state_object(
            'agent', intent, request_slots, inform_slots)
        state_tracker = self.__slot_intent_state_context.update_state_tracker(
            state_tracker)

        answer = state_tracker.get_answer()
        if answer:
            print('answer ', answer)
            state_tracker.reset_answer()
            state_tracker.remove_user_requests(
                list(state_tracker.get_first_user_request().keys())[0])
            if state_tracker.get_first_user_request() is None:
                state_tracker.reset()

        question = state_tracker.get_cur_action()
        if question:
            print('question ', question)

        self.__redis.set_key_value(user_id + ':db_helper', pickle.dumps(state_tracker.db_helper))
        delattr(state_tracker, 'db_helper')
        self.__redis.set_key_value(user_id + ':state_tracker', pickle.dumps(state_tracker))
        return answer if answer else question, user_id

    def make_response_sentence(self, data):
        raw_intent = data.get('intent', False)
        
        if raw_intent in ['request', 'inform']:
            intent = None
            value = None
            if raw_intent == 'request':
                request_slots = list(data.get('request_slots', False).items())[0]
                intent = request_slots[0].replace(':', '_') + '_' + raw_intent

            if raw_intent == 'inform':
                inform_slots = list(data.get('inform_slots', False).items())[0]
                intent = inform_slots[0].replace(':', '_')
                value = inform_slots[1]

            sentence = self.get_pattern_responce_sentence(intent)

            return sentence.replace('KEYWORD', value if value else '')

        elif raw_intent in ['complete', 'thanks', 'done']:
            sentence = self.get_pattern_responce_sentence('complete')
            return sentence
        
        elif raw_intent == 'greeting':
            sentence = self.get_pattern_responce_sentence('greeting')
            return sentence

    def get_pattern_responce_sentence(self, intent):
        return random.sample(getattr(pattern_responce_sentence, intent), 1)[0]

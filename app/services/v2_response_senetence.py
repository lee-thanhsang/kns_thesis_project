# import pattern_responce_sentence as pattern_responce_sentence
import services.pattern_responce_sentence as pattern_responce_sentence
import random
from utils.state_tracker.state_tracker import StateTracker
from utils.state_tracker.intent_slot_state import *
# import intent_slot_service.client as intent_slot_service

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
        self.__state_tracker = StateTracker()
        

    def get_intent_and_slot_from_sentence(self, message):
        state_tracker = self.__state_tracker
        
        intent, slot = self.__intent_slot_svc_cli.get_intent_and_slot(message)
        
        inform_slots = slot
        request_slots = {}
        if intent not in ['inform', 'greeting', 'complete', 'meaningless']:
            request_slots = {intent: 'UNK'}
            intent = 'request'

        self.__slot_intent_state_context.set_state_object('user', intent, request_slots, inform_slots)
        state_tracker = self.__slot_intent_state_context.update_state_tracker(state_tracker)
        self.__state_tracker = state_tracker
        

        state = state_tracker.get_state()
        action = self.__action_decider_svc_cli.get_action(state)

        
        intent = action['intent']
        request_slots = action['request_slots']
        inform_slots = action['inform_slots']
        self.__slot_intent_state_context.set_state_object('agent', intent, request_slots, inform_slots)
        state_tracker = self.__slot_intent_state_context.update_state_tracker(state_tracker)
        self.__state_tracker = state_tracker

        print(vars(state_tracker))


        # answer = state_tracker.get_answer()
        # if answer:
        #     print(answer)
        #     state_tracker.reset_answer()
        #     state_tracker.remove_user_requests(state_tracker.get_first_user_request())
        #     if state_tracker.get_first_user_request() is None:
        #         state_tracker.reset()

        #     return
            
        return '1'
    


    # def make_response_sentence(self, data):
    #     raw_intent = data.get('intent', False)
    #     inform_slots = list(data.get('inform_slots', False).items()) if data.get('inform_slots', False) else []
    #     request_slots = list(data.get('request_slots', False).items()) if data.get('request_slots', False) else []

    #     intent = None
    #     value = None
    #     if raw_intent == 'request':
    #         intent = request_slots[0][0] + '_' + raw_intent

    #     if raw_intent == 'inform':
    #         intent = inform_slots[0][0]
    #         value = inform_slots[0][1]

    #     pattern_sentence = random.sample(getattr(pattern_responce_sentence, intent), 1)[0]
    #     return pattern_sentence.replace('KEYWORD', value if value else '')

    # def output_responce_sentence(self, sentence):
    #     data = self.get_intent_and_slot_from_sentence(sentence)
    #     responce_sentence = self.make_response_sentence(data)
    #     return responce_sentence

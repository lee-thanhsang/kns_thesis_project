# import pattern_responce_sentence as pattern_responce_sentence
import app.services.pattern_responce_sentence as pattern_responce_sentence
import random

class V2ResponseSentenceService:
    def __init__(self):
        pass

    def get_intent_and_slot_from_sentence(self, sentence):
        inform_slot = random.sample([
            'fullname',
            'fullname_request',
            'contact',
            'host',
            'host_request',
            'job_description',
            'number',
            'register_way',
            'requirement',
            'benefit_drl',
            'benefit_ctxh',
            'benefit_others',
            'time_start',
            'time_end',
            'register_time_start',
            'register_time_end',
            'place',
            'place_request',
            'greeting',
            'complete'
        ], 1)[0]

        result = {
            'intent': 'inform',
            'inform_slots': {inform_slot: 'TEST DATA'},
            'request_slots': {'place': 'UNK'}
        }
        return result
    
    def make_response_sentence(self, data):
        raw_intent = data.get('intent', False)
        inform_slots = list(data.get('inform_slots', False).items()) if data.get('inform_slots', False) else []
        request_slots = list(data.get('request_slots', False).items()) if data.get('request_slots', False) else []

        intent = None
        value = None
        if raw_intent == 'request':
            intent = request_slots[0][0] + '_' + raw_intent

        if raw_intent == 'inform':
            intent = inform_slots[0][0]
            value = inform_slots[0][1]

        pattern_sentence = random.sample(getattr(pattern_responce_sentence, intent), 1)[0]
        return pattern_sentence.replace('KEYWORD', value if value else '')

    def output_responce_sentence(self, sentence):
        data = self.get_intent_and_slot_from_sentence(sentence)
        responce_sentence =  self.make_response_sentence(data)
        return responce_sentence

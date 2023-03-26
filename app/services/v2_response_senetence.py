# import pattern_responce_sentence as pattern_responce_sentence
import app.services.pattern_responce_sentence as pattern_responce_sentence
import random
# import intent_slot_service.client as intent_slot_service

class V2ResponseSentenceService:
    def __init__(self):
        pass

    def get_intent_and_slot_from_sentence(self, sentence):
        return intent_slot_service.main(sentence)

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

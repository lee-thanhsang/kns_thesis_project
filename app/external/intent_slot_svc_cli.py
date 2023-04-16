import grpc
import underthesea
import json
import sys

from proto.intent_slot_service_pb2_grpc import ISServiceStub
from proto.intent_slot_service_pb2 import IntentSlotRecognizeRequest

class IntentSlotServiceClient:
    def __init__(self, config):
        channel = grpc.insecure_channel(config['intent_slot_service']['url'])
        self.__stub = ISServiceStub(channel)

    def get_intent_and_slot(self, message):
        message = underthesea.word_tokenize(message, format='text')
        res = self.__stub.IntentSlotRecognize(IntentSlotRecognizeRequest(message=message))
        data = json.loads(res.message)
        return (data['intent'], data['slot'])
    
    
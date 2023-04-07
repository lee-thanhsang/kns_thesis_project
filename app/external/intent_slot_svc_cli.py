import grpc
import underthesea
import json
import sys
sys.path.append('../intent_slot_service')

import intent_slot_service_pb2_grpc
import intent_slot_service_pb2

class IntentSlotServiceClient:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:5002')
        self.__stub = intent_slot_service_pb2_grpc.ISServiceStub(channel)

    def get_intent_and_slot(self, message):
        message = underthesea.word_tokenize(message, format='text')
        res = self.__stub.IntentSlotRecognize(intent_slot_service_pb2.IntentSlotRecognizeRequest(message=message))
        data = json.loads(res.message)
        return (data['intent'], data['slot'])
    
    
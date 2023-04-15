import grpc
import underthesea
import json
import sys
import numpy as np

from proto.action_decider_service_pb2_grpc import ACServiceStub
from proto.action_decider_service_pb2 import DialogState

class ActionDeciderServiceClient:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:5003')
        self.__stub = ACServiceStub(channel)

    def get_action(self, state):
        converted_state = np.array(state, dtype=np.float32).tobytes()
        res = self.__stub.ActionDecider(DialogState(state = converted_state))
        return json.loads(res.action)
    
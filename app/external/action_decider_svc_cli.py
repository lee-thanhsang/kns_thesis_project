import grpc
import underthesea
import json
import sys
import numpy as np

sys.path.append('C:/thesis/kns_fecth_data/action_decider_service')

import action_decider_service_pb2_grpc
import action_decider_service_pb2

class ActionDeciderServiceClient:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:5003')
        self.__stub = action_decider_service_pb2_grpc.ACServiceStub(channel)

    def get_action(self, state):
        converted_state = np.array(state, dtype=np.float32).tobytes()
        res = self.__stub.ActionDecider(action_decider_service_pb2.DialogState(state = converted_state))
        return json.loads(res.action)
    
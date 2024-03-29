import grpc
import underthesea
import json
import sys
import numpy as np

from proto.action_decider_service_pb2_grpc import ACServiceStub
from proto.action_decider_service_pb2 import DialogState

class ActionDeciderServiceClient:
    def __init__(self, config):
        if 'localhost' in config['action_decider_service']['url']:
            channel = grpc.insecure_channel(config['action_decider_service']['url'])
        else:
            credentials = grpc.ssl_channel_credentials()
            channel = grpc.secure_channel(config['action_decider_service']['url'], credentials)
        self.__stub = ACServiceStub(channel)

    def get_action(self, state):
        converted_state = np.array(state, dtype=np.float32).tobytes()
        res = self.__stub.ActionDecider(DialogState(state = converted_state))
        return json.loads(res.action)
    
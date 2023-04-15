from external import *
from services import *
from utils.cache import *

class Server:
    def __init__(self):
        self.__intent_slot_svc_cli = intent_slot_svc_cli.IntentSlotServiceClient()
        self.__action_decider_svc_cli = action_decider_svc_cli.ActionDeciderServiceClient()
        self.__redis = redis.Redis()

        self.v2_response_sentence = v2_response_senetence.V2ResponseSentenceService(
            self.__intent_slot_svc_cli,
            self.__action_decider_svc_cli,
            self.__redis
        )

server = Server()
from external import *
from services import *
from utils.cache import *
from utils.clickhouse_client.clickhouse_client import *

class Server:
    def __init__(self):
        self.__intent_slot_svc_cli = intent_slot_svc_cli.IntentSlotServiceClient()
        self.__action_decider_svc_cli = action_decider_svc_cli.ActionDeciderServiceClient()
        self.__redis = redis.Redis()
        self.__clickhouse_client = ClickhouseClient()

        self.v2_response_sentence = v2_response_senetence.V2ResponseSentenceService(
            self.__intent_slot_svc_cli,
            self.__action_decider_svc_cli,
            self.__redis,
            self.__clickhouse_client
        )

server = Server()
from external.action_decider_svc_cli import *
from external.intent_slot_svc_cli import *
from external.post_slot_svc_cli import *
from services import *
from utils.cache.redis import *
from utils.clickhouse_client.clickhouse_client import *
from utils.es_client.es_client import *
from conf.config import *
from services.v2_response_senetence import *
from services.v2_crawler_data_services import *
from pymessenger.bot import Bot


class Server:
    def __init__(self):
        print('INIT')
        self.__config = Config()
        config = self.__config.get()
        self.__es_client = EsClient(config)
        self.__intent_slot_svc_cli = IntentSlotServiceClient(config)
        self.__post_slot_svc_cli = PostSlotServiceClient(config)
        self.__action_decider_svc_cli = ActionDeciderServiceClient(config)
        self.redis = Redis(config)
        self.clickhouse_client = ClickhouseClient(config)


        self.v2_response_sentence = V2ResponseSentenceService(
            self.__intent_slot_svc_cli,
            self.__action_decider_svc_cli,
            self.redis,
            self.clickhouse_client
        )

        self.v2_process_post_slot = V2CrawlDataService(
            self.__post_slot_svc_cli,
            self.__es_client
        )

server = Server()
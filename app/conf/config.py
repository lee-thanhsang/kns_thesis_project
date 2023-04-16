import yaml
import os

CONFIG_FILE = 'conf/config.dev.yaml'

class Config:
    def __init__(self):
        with open(CONFIG_FILE) as yamlfile:
            file_config = yaml.load(yamlfile, Loader=yaml.FullLoader)

        self.__config = {}
        
        self.__config['app'] = {}
        self.__config['app']['host'] = os.getenv('APP__HOST') or file_config['app']['host']
        self.__config['app']['port'] = os.getenv('APP__PORT') or file_config['app']['port']
        
        self.__config['database'] = os.getenv('DATABASE') or file_config['database']

        self.__config['intent_slot_service'] = {}
        self.__config['intent_slot_service']['url'] = os.getenv('INTENT_SLOT_SERVICE__URL') or file_config['intent_slot_service']['url']

        self.__config['action_decider_service'] = {}
        self.__config['action_decider_service']['url'] = os.getenv('ACTION_DECIDER_SERVICE__URL') or file_config['action_decider_service']['url']
        
        self.__config['redis'] = {}
        self.__config['redis']['host'] = os.getenv('REDIS__HOST') or file_config['redis']['host']
        self.__config['redis']['port'] = os.getenv('REDIS__PORT') or file_config['redis']['port']

        self.__config['clickhouse'] = {}
        self.__config['clickhouse']['host'] = os.getenv('CLICKHOUSE__HOST') or file_config['clickhouse']['host']
        self.__config['clickhouse']['port'] = os.getenv('CLICKHOUSE__PORT') or file_config['clickhouse']['port']
        self.__config['clickhouse']['username'] = os.getenv('CLICKHOUSE__USERNAME') or file_config['clickhouse']['username']
        self.__config['clickhouse']['password'] = os.getenv('CLICKHOUSE__PASSWORD') or file_config['clickhouse']['password']

        self.__config['elasticsearch'] = os.getenv('ELASTICSEARCH') or file_config['elasticsearch']

    def get(self):
        return self.__config
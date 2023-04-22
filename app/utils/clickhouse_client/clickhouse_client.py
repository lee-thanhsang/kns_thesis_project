import clickhouse_connect

DIALOG_ORDER = ['user_id', 'is_cache', 'raw_request', 'intent', 'slot', 'reformed_slot',
                'state', 'action', 'raw_response', 'current_informs', 'history', 'confirmation', 'wrong_decision']


class ClickhouseClient:
    def __init__(self, config):
        self.__client = clickhouse_connect.get_client(
            host=config['clickhouse']['host'], 
            username=config['clickhouse']['username'], 
            password=config['clickhouse']['password'], 
            port=config['clickhouse']['port']
        )

    def create_dialog(self, log):
        log_list = []
        for field in DIALOG_ORDER:
            if field in log.keys():
                log_list.append(log[field])
            else:
                log_list.append(None)

        log_list = [log_list]
        self.__client.insert('dialog', log_list, column_names = DIALOG_ORDER)

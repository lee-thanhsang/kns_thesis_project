import clickhouse_connect

DIALOG_ORDER = ['user_id', 'is_cache', 'raw_request', 'intent', 'slot', 'reformed_slot',
                'state', 'action', 'raw_response', 'current_informs', 'history']


class ClickhouseClient:
    def __init__(self):
        print('INIT')
        self.__client = clickhouse_connect.get_client(
            host='xe9pfzmzgi.eu-west-1.aws.clickhouse.cloud', username='default', password='JZDfmD8IAwxJ~', port=8443
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

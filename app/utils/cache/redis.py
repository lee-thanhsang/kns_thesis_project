import redis


class Redis:
    def __init__(self, config):
        self.__redis = redis.Redis(host=config['redis']['host'], port=config['redis']['port'], password=config['redis']['password'])

    def set_key_value(self, key: str, value: str, ex=600):
        self.__redis.set(key, value, ex=ex)

    def get_value_from_key(self, key: str) -> str:
        return self.__redis.get(key)
    
    def remove_by_key(self, key: str):
        return self.__redis.delete(key)

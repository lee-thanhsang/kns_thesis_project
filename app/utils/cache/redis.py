import redis


class Redis:
    def __init__(self):
        self.__redis = redis.from_url('redis://localhost:6379')

    def set_key_value(self, key: str, value: str):
        self.__redis.set(key, value, ex=900)

    def get_value_from_key(self, key: str) -> str:
        return self.__redis.get(key)

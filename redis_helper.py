from redis import Redis


class RedisTools:

    def __init__(self, host='redis', port=6379, db=0, decode_responses=True) -> None:
        self.redis_connect = Redis(host=host, port=port, db=db, decode_responses=decode_responses)

    def set_pair(self, currency: str, price: str) -> None:
        self.redis_connect.set(currency, price)

    def get_pair(self, currency: str) -> str:
        return self.redis_connect.get(currency)

    def pairs(self):
        return self.redis_connect.keys(pattern='*')


redis_db = RedisTools()

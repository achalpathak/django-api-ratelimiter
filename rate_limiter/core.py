from django.conf import settings
import redis
from rest_framework.exceptions import ValidationError

redis_client = None


def connect_redis():
    """
    Establishing connection with Redis
    """
    global redis_client
    if not redis_client:
        # get credentials from environment variables
        redis_client = redis.Redis(
            host=settings.REDIS_SETTINGS["REDIS_HOST"],
            port=settings.REDIS_SETTINGS["REDIS_PORT"],
            db=settings.REDIS_SETTINGS["REDIS_DB"],
            password=settings.REDIS_SETTINGS["REDIS_PASSWORD"],
        )
    assert redis_client.ping()  # check if connection is successful
    return redis_client


class RateLimiter:
    def __init__(self):
        self._db = connect_redis()

    def parse_key(self, request, key):
        if key.lower() == "ip":
            return request.META["REMOTE_ADDR"]  # return IP of the user
        elif "header" in key.lower():
            header_value = key.split(":")[1]
            return request.META.get(f"HTTP_{header_value.replace('-','_')}", "")
        else:
            raise ValidationError(f"Invalid key supplied. {key}")

    def parse_rate(self, rate):
        time_periods = {
            "s": 1,
            "m": 60,
            "h": 60 * 60,
            "d": 24 * 60 * 60,
        }
        count, unit = rate.split("/")
        return int(count), time_periods[unit]

    def is_rateLimited(self, request, key, rate):
        key = self.parse_key(request, key)
        count, unit = self.parse_rate(rate)
        print(count, "   ", unit)
        if int(self._db.incr(key)) > count:
            return True
        if self._db.ttl(key) == -1:  # timeout is not set
            self._db.expire(key, unit)
            return False
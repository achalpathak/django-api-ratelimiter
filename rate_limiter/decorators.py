from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from .core import RateLimiter as RateLimiterService


def rate_limiter(key, rate):
    def _rate_limiter(function):
        def __rate_limiter(*args, **kwargs):
            if getattr(
                settings, "RATE_LIMITING_ENABLED"
            ):  # checks global settings for rate limiting
                if RateLimiterService().is_rateLimited(
                    request=args[0].request, key=key, rate=rate
                ):
                    raise RateLimitExceeded
            return function(*args, *kwargs)

        return __rate_limiter

    return _rate_limiter


class RateLimitExceeded(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = getattr(
        settings,
        "RATE_LIMITING_MSG",
        "Request was throttled. Too many requests. Please wait.",
    )
    default_code = "throttled"

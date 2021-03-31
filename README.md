# Version Requirements
<img src="https://img.shields.io/badge/Django-3.1.7-blue?style=for-the-badge">   <img src="https://img.shields.io/badge/Redis-3.5.3-red?style=for-the-badge">   <img src="https://img.shields.io/badge/DjangoRedis-4.12.1-green?style=for-the-badge"> 


# Description

Django API RateLimiter is a rate-limiting decorator for Django APIs using Redis as a caching layer to speed up the checking and updating of API hits made by a user


## Configure Settings

```python
# Configure Redis Cache Backend
REDIS_SETTINGS = {
    "REDIS_HOST": "localhost",
    "REDIS_PORT": "6379",
    "REDIS_DB": "1",
    "REDIS_PASSWORD": "",
}

# Configure enable/disable rate limiting
RATE_LIMITING_ENABLED = True 

# Configure rate-limiting error message
RATE_LIMITING_MSG = "Request was throttled. Too many requests. Please wait."
```

## Usage
Example 1
```python
from rate_limiter.decorators import rate_limiter

@rate_limiter(key="ip", rate="5/m")
def myview(request):
    # Allows 5 requests per minute per IP.
    pass
```

Example 2
```python
from rate_limiter.decorators import rate_limiter

@rate_limiter(key="header:X-Client-Code", rate="35/s")
def myview(request):
    # Allows 35 requests per second per X-Client-Code header.
    pass
```

## Keys and Rate Configurations
KEYS
```python
'ip' - Use the request IP address (i.e. request.META['REMOTE_ADDR'])
'header:X-X' - Use the value of request.META.get('HTTP_X_X', '')
```

RATE
```python
's' - second
'm' - minute
'h' - hour
'd' - day
Example
'100/s' - Limits requests to 100 per second
'45/h' - Limits requests to 45 per hour
```

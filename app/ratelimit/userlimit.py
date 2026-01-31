"""
    Perform Redis atomic operation.
"""
import time
import uuid
from core.redis import redis_client

WINDOW = 60
r = redis_client # call 'r' for every cmd to interact with redis
LIMIT = 10

def validate_user_limit(user_ip) -> bool:
    response = False

    # Build Redis key
    unique_key = f"rate_limit:ip:{user_ip}"

    # Get current timestamp
    NOW = int(time.time()*1000) #milliseconds

    # Add timestamp to ZSET
    r.zadd(unique_key, {f"req:{uuid.uuid4()}":NOW})

    # Remove old timestamps
    old_timestamp = NOW - WINDOW
    r.zremrangebyscore(unique_key, "-inf", old_timestamp)

    count = r.zcard(unique_key)
    

    if count <= LIMIT:
        response = True

    r.expire(unique_key, WINDOW*2)

    return response







"""
    Perform Redis atomic operation.
"""
import time
import uuid
from math import ceil
from core.redis import redis_client

r = redis_client # call 'r' for every cmd to interact with redis

lua_script = """
local info = {0, 0}
local unique_key = KEYS[1]
local limit = tonumber(ARGV[1])
local window_ms = tonumber(ARGV[2])
local NOW_MS = tonumber(ARGV[3])
local req_id = ARGV[4]
local old_timestamp = NOW_MS - window_ms

redis.call("ZREMRANGEBYSCORE", unique_key, "-inf", old_timestamp)

local count = redis.call("ZCARD", unique_key)

if count < limit then
    local message = "req:" .. req_id
    redis.call("ZADD", unique_key, NOW_MS, message)
    info[1] = 1
else
    local oldest = redis.call("ZRANGE", unique_key, 0, 0, "WITHSCORES")
    local oldest_score = tonumber(oldest[2])
    local retry_after_ms = (oldest_score + window_ms) - NOW_MS
    local retry_after_sec = math.ceil(retry_after_ms/1000)
    info[2] = math.max(0, retry_after_sec)
end
redis.call("EXPIRE", unique_key, math.floor((window_ms * 2) / 1000))

return info
"""
WINDOW_SEC = 60*60
LIMIT = 60
def validate_user_limit(user_ip) -> dict:
    info = {'allow':True, 'Retry-After':0}
    # Build Redis key
    unique_key = f"rate_limit:ip:{user_ip}"
    req_id = str(uuid.uuid4())

    NOW_MS = int(time.time()*1000) #milliseconds

    my_script = r.register_script(lua_script)
    result = my_script(
        keys=[unique_key],
        args=[LIMIT, WINDOW_SEC*1000, NOW_MS, req_id]
    )

    if result[0] == 0:
        info['allow'] = False
        info['Retry-After'] = result[1]


    return info







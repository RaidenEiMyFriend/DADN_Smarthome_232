import redis

# Connect to the local Redis instance
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
print(redis_client)


def get_redis_client():
    return redis_client



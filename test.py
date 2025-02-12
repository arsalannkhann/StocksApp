import redis

redis_url = "redis://localhost:6379"
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

# Test connection
print(redis_client.ping())  # Should return True if Redis is running
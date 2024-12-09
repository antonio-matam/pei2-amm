"""Module to encapsulate risk operations with the database"""
import sys
import redis
import uuid
import os

redis_client = redis.StrictRedis(
    host=os.environ["REDISHOST"],
    port=os.environ["REDISPORT"],
    decode_responses=True
)


def load(risk_id: uuid.UUID):
    """Load a risk from the database"""
    risk = redis_client.hgetall(str(risk_id))
    return risk


def save_risk(risk_id=None, **risk_description):
    """Insert a new risk associated with a city"""
    if not risk_id:
        risk_id = uuid.uuid4()

    redis_key = str(risk_id)
    risk = risk_description["risk"]
    level = risk_description["level"]
    city_name = risk_description["city_name"]
    print(f"risk_id= {redis_key} risk={risk} with level={level} in city={city_name}", file=sys.stderr)

    redis_client.hset(redis_key, mapping=risk_description)
    redis_client.expire(redis_key, 10)

    return {"risk_id": redis_key, **risk_description}

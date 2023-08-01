"""
Redis functions.

Redis connection and utility functions.
"""
import sys
from datetime import datetime

import redis
def get_redis_connection(host, port=6379, password=None):
# def get_redis_connection(redis_server, redis_port=6378, redis_password=""):
    """
    Return a connection to a Redis host if defined.
    """
    redis_connection = None
    if host:
        try:
            print(f"Connect to Redis service on {host}.")
            redis_connection = redis.Redis(
                host = host,
                port = port,
                password = password
                )
            redis_connection.set("connected", datetime.now().isoformat(sep=' '))
        except redis.ConnectionError as err:
            print(f"Error creating Redis connection: {err}", file=sys.stderr)
            redis_connection = None

    return redis_connection


def increment_redis_counter(redis_connection, counter='counter'):
    """
    Increase a counter variable in Redis.

    Args:
        redis_connection: A Redis connection
        counter: The name of the variable to be increased, defaults to counter.
    """
    value = 0
    if redis_connection:
        try:
            if redis_connection.get(counter):
                cnt = int(redis_connection.get(counter)) + 1
                redis_connection.set(counter, cnt)
                value = cnt
            else:
                redis_connection.set(counter, "1")
                value = 1
        except redis.ConnectionError as err:
            print(f"Error connecting to Redis: {err}", file=sys.stderr)
    print(f"page_views: {value}", file=sys.stderr)
    return value


def get_redis_counter(redis_connection, counter='counter'):
    """
    Read a counter from Redis.

    Args:
        redis_connection: A Redis connection
        counter: The name of the variable to be increased, defaults to counter.
    """
    value = 0
    if redis_connection:
        try:
            value = redis_connection.get(counter)
        except redis.ConnectionError as err:
            print(f"Error connecting to Redis: {err}", file=sys.stderr)
    return value

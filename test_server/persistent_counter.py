"""
Redis functions.

Redis connection and utility functions.
"""
import redis
import sys

def get_redis_connection(host, port=6379, password=None):
# def get_redis_connection(redis_server, redis_port=6378, redis_password=""):
    """
    Return a connection to a Redis host if defined.
    """
    redis_connection = None
    if host:
        try:
            print("Connect to Redis service on {}".format(host))
            # redis_connection = redis.from_url(redis_url,)
            redis_connection = redis.Redis(
                host = host,
                port = port,
                password = password
                )

        except Exception as exc:
            print("Error connecting to Redis: {}".format(exc), file=sys.stderr)
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
        except Exception as exc:
            print("Error connecting to Redis: {}".format(exc), file=sys.stderr)
    print("page_views: {}".format(value), file=sys.stderr)
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
        except Exception as exc:
            print("Error connecting to Redis: {}".format(exc), file=sys.stderr)
    return value

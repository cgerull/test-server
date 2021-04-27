import os


class Config(object):
    """Read and set configuration values"""
    DEBUG = os.environ.get('DEBUG') or False
    TESTING = os.environ.get('TESTING') or False

    APP_NAME = os.environ.get('APP_NAME') or 'Test server'
    APP_FOOTER = os.environ.get('APP_FOOTER') or 'Default configuration'
    PONG = os.environ.get('PONG') or 'Testserver is alive'

    SECRET_FILE = os.environ.get('SECRET_FILE') or '/run/secrets/my_secret_key'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Only_the_default_secret_key'
    CONFIG_FILE = os.environ.get('SECRET_KEY') or './srv-config.yml'
    
    ACCESS_LOG = os.environ.get('ACCESS_LOG') or None
    ERROR_LOG = os.environ.get('ERROR_LOG') or None
    LOG_LINES = os.environ.get('LOG_LINES') or 30
    
    REDIS_URL = os.environ.get("REDIS_URL") or None
    REDIS_SERVER = os.environ.get('REDIS_SERVER') or None
    REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
    REDIS_HTML_COUNTER = os.environ.get('REDIS_HTML_COUNTER') or'api_srv_html_counter'
    REDIS_API_COUNTER = os.environ.get('REDIS_API_COUNTER') or'api_srv_counter'

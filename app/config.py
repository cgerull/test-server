import os


class Config(object):
    """Read and set configuration values"""
    DEBUG = False
    TESTING = False

    APP_NAME = 'Test server'
    APP_FOOTER = 'Default configuration'

    SECRET_KEY = 'Only_the_default_secret_key'
    SECRET_FILE = '/run/secrets/my_secret_key'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Only_the_default_secret_key'
    CONFIG_FILE = './srv-config.yml'
    
    ACCESS_LOG = os.environ.get('ACCESS_LOG') or None
    ERROR_LOG = os.environ.get('ERROR_LOG') or None
    LOG_LINES = 30
    
    REDIS_URL = os.environ.get("REDIS_URL") or None
    REDIS_SERVER = os.environ.get('REDIS_SERVER') or None
    REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
    REDIS_HTML_COUNTER = 'api_srv_html_counter'
    REDIS_API_COUNTER = 'api_srv_counter'

    # def get_secret_file():
    #     return  _SECRET_FILE
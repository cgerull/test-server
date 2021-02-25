import os


class Config(object):
    """Read and set configuration values"""
    SECRET_KEY = 'Only_the_default_secret_key'
    SECRET_FILE = '/run/secrets/my_secret_key'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Only_the_default_secret_key'
    CONFIG_FILE = './srv-config.yml'


    # def get_secret_file():
    #     return  _SECRET_FILE
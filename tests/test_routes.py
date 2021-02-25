import os
import pytest
from app import routes


def test_get_secret_key():
    assert routes.get_secret_key() == 'Only_the_default_secret_key'

def test_read_config_no_file():
    config_items = len(routes.srv_config)
    routes.read_config(routes.config_file, routes.srv_config)
    assert config_items == len(routes.srv_config)

def test_read_config_with_file():
    config_items = len(routes.srv_config)
    routes.read_config('example-srv-config.yml', routes.srv_config)
    assert config_items != len(routes.srv_config)
    assert 11 == len(routes.srv_config)


# def test_get_secret_key_from_file(tmpdir):
#     file = 'mysecret'
#     f = tmpdir.join(file)
#     f.write('my_test_file_secret')
#     print("f: {}".format(str(f)))
#     assert routes.get_secret_key(str(f)) == 'my_test_file_secret'
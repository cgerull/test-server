import os
import pytest
from app import routes


def test_get_secret_key():
    assert routes.get_secret_key() == 'Only_the_default_secret_key'


# def test_get_secret_key_from_file(tmpdir):
#     file = 'mysecret'
#     f = tmpdir.join(file)
#     f.write('my_test_file_secret')
#     print("f: {}".format(str(f)))
#     assert routes.get_secret_key(str(f)) == 'my_test_file_secret'
from app import Config
import os
import pytest

def test_SECRET():
    assert Config.SECRET_KEY == 'Only_the_default_secret_key'

def test_SECRET_FILE():
    assert Config.SECRET_FILE == '/run/secrets/my_secret_key'
    
# def test_SECRET_with_env(monkeypatch):
#     monkeypatch.setenv("SECRET_KEY", "MonkeySecret")
#     print("KEY: {}".format(os.getenv('SECRET_KEY')))
#     assert Config.get_secret_key() == 'MonkeySecret'
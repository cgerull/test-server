import os
import pytest
from app import app

def test_check_config_length():
    assert 'ping' != app.config['PONG']

def test_check_config_name():
    assert 'Test server' == app.config['APP_NAME']
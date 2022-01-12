import os
import pytest
from app import app

def test_check_config_length():
    assert 'ping' != app.config['PONG']

def test_check_config_app_name():
    assert 'Test server' == app.config['APP_NAME']

def test_check_config_redis_service():
    assert None == app.config['REDIS_SERVER']

def test_check_config_redis_port():
    assert 6379 == app.config['REDIS_PORT']

def test_check_config_redis_html_counter():
    assert 'api_srv_html_counter' == app.config['REDIS_HTML_COUNTER']

def test_check_config_db_type():
    assert 'sqlite' == app.config['DB_TYPE']

def test_check_config_database():
    assert 'test_server' == app.config['DATABASE']
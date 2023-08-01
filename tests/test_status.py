"""
Test status page
"""
import pytest
from flask import g, session

def test_status_response(client, auth):
    """ Happy flow, status page with login."""
    response = auth.login()
    assert '/' == response.headers['Location']
    assert client.get('/status').status_code == 200
    # pass


def test_status_no_login_response(client):
    """ Happy flow, status page without login."""
    assert client.get('/status').status_code == 302
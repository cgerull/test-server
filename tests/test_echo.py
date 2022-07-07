"""
Test echo page
"""
# import pytest
# from test_server.db import get_db

def test_echo_response(client):
    """ Happy flow, echo page."""
    assert client.get('/echo').status_code == 200


def test_echo_index_response(client):
    """ Happy flow, index redirect."""
    assert client.get('/').status_code == 302

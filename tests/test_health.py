
HEALTH_ENDPOINT = '/health'

def test_health_ok_response(client):
    """ Happy flow, health page."""
    assert client.get(HEALTH_ENDPOINT).status_code == 200
    assert client.get(HEALTH_ENDPOINT).data == b"testserver is healthy."

def test_health_bad_response(unhealthy_client):
    """ Error flow, health page."""
    assert unhealthy_client.get(HEALTH_ENDPOINT).status_code == 500
    assert unhealthy_client.get(HEALTH_ENDPOINT).data == b"(DB: ERROR! Can't connect to database. no such table: req_log)"

from test_server import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True, 'DB_TYPE': None}).testing


def test_hello(client):
    response = client.get('/health')
    assert response.data == b'test_server is healthy.'
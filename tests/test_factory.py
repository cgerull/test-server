'''
Test general app creation functions
'''
from test_server import create_app


def test_config():
    ''' Test app config loading. '''
    assert not create_app().testing
    assert create_app({'TESTING': True, 'DB_TYPE': None}).testing

def test_app_defaults():
    ''' Test default db name.'''
    app = create_app()
    assert 'sqlite' == app.config['DB_TYPE']
    assert 'testserver' == app.config['DB_NAME']

def test_hello(client):
    ''' Test health endpoint. '''
    response = client.get('/health')
    assert response.data == b'testserver is healthy.'

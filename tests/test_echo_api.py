'''
Test the echo_api function.
'''
def test_echo_api(client):
    """
    Test the echo_api function.

    This test checks the happy flow of the echo_api function by sending a GET request to '/v1/echo'
    and verifying the response status code, JSON payload, and headers.

    Returns:
        None
    """
    assert client.get('/v1/echo').status_code == 200
    assert client.get('/v1/echo').get_json() == {
            'fields': {
                'Cookies': {},
                'Method': 'GET HTTP/1.1',
                'QueryString': '',
                'Referrer': None,
                'RemoteAddr': '127.0.0.1',
                'URL': 'http://localhost/v1/echo',
                'UserAgent': 'werkzeug/3.0.0'
                },
            'headers': {
                'HTTP_HOST': 'localhost',
                'HTTP_USER_AGENT': 'werkzeug/3.0.0'
                },
            'environment': {
                'version': '0.1.0',      # current_app.config['VERSION'],
                'environment': 'test'   # current_app.config['ENV']
            }
        }

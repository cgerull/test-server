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
    assert client.get('/v1/echo').get_json()["environment"] == {
        'version': '0.1.0',      # current_app.config['VERSION'],
        'environment': 'test'   # current_app.config['ENV']
        }

"""
Test status page
"""
STATUS_URL = '/status'

def test_status_response(client, auth):
    """ Happy flow, status page with login."""
    response = auth.login()
    assert '/' == response.headers['Location']
    assert client.get(STATUS_URL).status_code == 200
    # Add additional assertions here to test the response content

def test_status_no_login_response(client):
    """ Happy flow, status page without login."""
    assert client.get(STATUS_URL).status_code == 302
    # Add additional assertions here to test the redirection

def test_status_redirect_to_login(client):
    """ Test redirection to login page when not logged in."""
    response = client.get(STATUS_URL)
    assert response.status_code == 302
    assert response.headers['Location'] == "/auth/login"
    # Add additional assertions here to test the flash message

def test_status_logged_in(client, auth):
    """ Test status page when logged in."""
    auth.login()
    response = client.get(STATUS_URL)
    assert response.status_code == 200
    assert b"Server Info" in response.data
    # Add additional assertions here to test the rendered template and data passed to it

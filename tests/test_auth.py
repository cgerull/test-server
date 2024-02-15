"""
Unit tests for the authentication functionality.
"""
import pytest
from flask import g, session
from test_server.db import get_db

REGISTER_URL = '/auth/register'

def test_register(client, app):
    """
    Test the registration functionality.

    This function tests the registration process by sending a POST request to the registration URL
    with a username and password. It then checks if the response redirects to the login page and
    verifies that the user is successfully added to the database.

    Args:
        client: The test client for making HTTP requests.
        app: The Flask application object.

    Returns:
        None
    """
    assert client.get(REGISTER_URL).status_code == 200
    response = client.post(
        REGISTER_URL, data={'username': 'a', 'password': 'a'}
    )

    assert '/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    """
    Test the registration form validation.

    Args:
        client (object): The test client for making HTTP requests.
        username (str): The username to be used for registration.
        password (str): The password to be used for registration.
        message (str): The expected error message.

    Returns:
        None
    """
    response = client.post(
        REGISTER_URL,
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    """
    Test the login functionality.

    This function tests the login functionality by performing the following steps:
    1. Sends a GET request to '/auth/login' and asserts that the response status code is 200.
    2. Calls the `login` method of the `auth` object and assigns the response
       to the `response` variable.
    3. Asserts that the value of the 'Location' header in the response is '/'.
    4. Uses the `client` object in a context manager to perform additional assertions:
       - Sends a GET request to '/'.
       - Asserts that the value of the 'user_id' key in the `session` object is 1.
       - Asserts that the value of the 'username' key in the `g.user` object is 'test'.
    """
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert '/' == response.headers['Location']

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    """
    Test the login function to validate the input.

    Args:
        auth (Auth): An instance of the Auth class.
        username (str): The username to be used for login.
        password (str): The password to be used for login.
        message (str): The expected message in the response data.

    Returns:
        None
    """
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    """
    Test the logout functionality.

    This function tests the logout functionality by performing the following steps:
    1. Logs in the user using the `auth.login()` method.
    2. Calls the `auth.logout()` method to log out the user.
    3. Asserts that the 'user_id' key is not present in the session.

    This test ensures that the logout process works correctly and removes the user's session data.

    Args:
        client: The test client for making requests.
        auth: The authentication helper object.

    Returns:
        None
    """
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

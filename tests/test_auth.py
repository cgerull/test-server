"""
Unit tests for the authentication functionality.
"""
"""
Tests for the authentication blueprint.
"""
import pytest
from flask import g, session
from test_server.db import get_db

REGISTER_URL = '/auth/register'
LOGIN_URL = '/auth/login'

def test_register(client, app):
    """
    Test the registration functionality.

    This function sends a GET request to the registration URL and verifies that
    the response status code is 200.
    Then, it sends a POST request to the registration URL with a username
    and password.
    It asserts that the response redirects to the login page.
    Finally, it checks the database to ensure that the user with the specified
    username has been created.

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

    assert LOGIN_URL == response.headers['Location']

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
        client (TestClient): The test client for making requests.
        username (str): The username to be registered.
        password (str): The password to be registered.
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
    2. Calls the `login` method of the `auth` object and assigns the response to
       the `response` variable.
    3. Asserts that the 'Location' header of the response is '/'.
    4. Uses the `client` object in a context manager to perform additional assertions:
       - Sends a GET request to '/'.
       - Asserts that the 'user_id' key in the session is equal to 1.
       - Asserts that the 'username' key in the 'g.user' dictionary is equal to 'test'.
    """
    assert client.get(LOGIN_URL).status_code == 200
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
    Test the login function to validate input.

    Args:
        auth (Auth): The Auth object used for authentication.
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
        auth: An instance of the authentication class.

    Returns:
        None
    """
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
# def test_register(client, app):
#     response = client.get('/auth/register')
#     assert response.status_code == 200

#     response = client.post('/auth/register', data={'username': 'a', 'password': 'a'})
#     assert response.headers['Location'] == LOGIN_URL

#     with app.app_context():
#         db = get_db()
#         user = db.execute("SELECT * FROM user WHERE username = 'a'").fetchone()
#         assert user is not None

# def test_register_validate_input(client):
#     response = client.post('/auth/register', data={'username': '', 'password': ''})
#     assert b'Username is required.' in response.data

#     response = client.post('/auth/register', data={'username': 'a', 'password': ''})
#     assert b'Password is required.' in response.data

#     response = client.post('/auth/register', data={'username': 'test', 'password': 'test'})
#     assert b'User test is already registered.' in response.data

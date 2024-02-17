'''
Test fixtures for the Flask application.
'''
import os

import pytest
from test_server import create_app
from test_server.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """
    Fixture that creates and configures a test Flask application.

    Returns:
        Flask: The test application instance.
    """
    app = create_app(
        {
            "TESTING": True,
            "ENV": "test",
            "SECRET_FILE": None,
            "SECRET_KEY": "unit_test",
            "DB_TYPE": "sqlite",
            "DB_PATH": "/tmp",
            "DB_NAME": "unit_test",
            "REDIS_SERVER": None,
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.unlink("/tmp/unit_test.sqlite")


@pytest.fixture
def unhealthy_app():
    """
    Fixture that creates and configures an unhealthy test Flask application.

    Returns:
        Flask: The unhealthy test application instance.
    """
    app = create_app(
        {
            "TESTING": True,
            "ENV": "test",
            "SECRET_FILE": None,
            "SECRET_KEY": "unit_test",
            "DB_TYPE": "sqlite",
            "DB_PATH": "/tmp",
            "DB_NAME": "unit_test",
            "REDIS_SERVER": None,
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
        os.unlink("/tmp/unit_test.sqlite")

    yield app

    os.unlink("/tmp/unit_test.sqlite")


@pytest.fixture
def client(app):
    """
    Fixture that provides a test client for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        FlaskClient: The test client.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Fixture that provides a test CLI runner for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        FlaskCliRunner: The test CLI runner.
    """
    return app.test_cli_runner()


@pytest.fixture
def unhealthy_client(unhealthy_app):
    """
    Fixture that provides a test client for the unhealthy Flask application.

    Args:
        unhealthy_app (Flask): The unhealthy Flask application instance.

    Returns:
        FlaskClient: The test client.
    """
    return unhealthy_app.test_client()


class AuthActions(object):
    """ Utility class for login simulation. """
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        """
        Simulates a login request.

        Args:
            username (str): The username.
            password (str): The password.

        Returns:
            Response: The response object.
        """
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        """
        Simulates a logout request.

        Returns:
            Response: The response object.
        """
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """
    Fixture that provides an instance of AuthActions for authentication simulation.

    Args:
        client (FlaskClient): The test client.

    Returns:
        AuthActions: The AuthActions instance.
    """
    return AuthActions(client)

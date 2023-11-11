import os

import pytest
from test_server import create_app
from test_server.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    # db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "ENV": "test",
            "SECRET_FILE": None,
            "SECRET_KEY": "unit_test",
            "DB_TYPE": "sqlite",
            "DB_PATH": "/tmp",
            "DB_NAME": "unit_test",
            # DATABASE=os.path.join(app.instance_path, 'test_server.sqlite'),
            # 'DATABASE': os.path.join(db_path, 'test_server.sqlite'),
            "REDIS_SERVER": None,
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # os.close(db_fd)
    # os.unlink(db_path)
    os.unlink("/tmp/unit_test.sqlite")


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    """ Utility class for login simulation. """
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)

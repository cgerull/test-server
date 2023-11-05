"""
Define and establish a database connection.
"""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# pylint: disable=E0237
def get_db():
    """
    TODO: Refactor for multiple database drivers.
    """
    if 'db' not in g:
        my_db= new_db()
        if my_db:
            g.db= my_db
        else:
            raise NameError("No valid database configured.")

    return g.db


def new_db():
    """ Create a database object. """
    my_db= None

    if 'sqlite' == current_app.config['DB_TYPE']:
        my_db= new_sqlite_db(current_app.config['DATABASE'])

    return my_db


def new_sqlite_db(db_name):
    """
    Create a new database. Drop old database if exists.
    TODO: Refactor for multiple database drivers.
    """
    sqlite_db = None

    try:
        sqlite_db = sqlite3.connect(
                db_name,
                detect_types=sqlite3.PARSE_DECLTYPES
        )
        sqlite_db.row_factory = sqlite3.Row
    except sqlite3.OperationalError as exc:
        print(f"ERROR! Can't connect to database. {exc}")

    return sqlite_db

def close_db(event=None):
    """
    If the a database object is on the  global stack, close that object.
    """
    my_db= g.pop('db', event)

    try:
        if isinstance(my_db, sqlite3.Connection):
        # if my_dbis not None:
            my_db.close()
    except sqlite3.OperationalError as exc:
        print(f"Error! Can't close database. {exc}")


def setup_db(my_db):
    """Add tables if not existing."""
    try:
        with current_app.open_resource('sql/schema.sql') as schema:
            my_db.executescript(schema.read().decode('utf8'))
    except sqlite3.OperationalError as exc:
        print(f"WARNING. Database already set. Caught {exc}")


def init_db():
    """
    Initialize database with the schema migrations.
    """
    my_db= get_db()
    try:
        with current_app.open_resource('sql/schema.sql') as schema:
            my_db.executescript(schema.read().decode('utf8'))
    except sqlite3.OperationalError as exc:
        print(f"WARNING! Initializing database. Caught {exc}")

def check_database():
    '''
    Test if the configured database is accessible and configured.
    '''
    result = {
        "pass": True,
        "msg": "OK"
    }
    my_db= get_db()
    if my_db is not None:
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(
                "SELECT * from req_log"
            )
        except my_db.OperationalError as err:
            result['pass'] = False
            result['msg'] = f"ERROR! Can't connect to database. {err}"
    return result


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """
    Inject init and teardown commands into flask app object.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

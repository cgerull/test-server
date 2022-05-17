import sqlite3
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    TODO: Refactor for multiple database drivers.
    """
    if 'db' not in g:
        db = new_db()
        if db:
            g.db = new_db()
        else:
            raise NameError("No valid database configured.")

    return g.db


def new_db():
    db = None

    if ('sqlite' == current_app.config['DB_TYPE']):
        db = new_sqlite_db(current_app.config['DATABASE'])

    return db


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
    except Exception as exc:
        print(f"ERROR! new_db caught {exc}")

    return sqlite_db

def close_db(e=None):
    """
    If the a database object is on the  global stack, close that object.
    """
    db = g.pop('db', e)

    try:
        if isinstance(db, sqlite3.Connection):
        # if db is not None:
            db.close()
    except Exception as exc:
        print(f"Error! close_db caught {exc}")


def setup_db(my_db):
    """Add tables if not existing."""
    try:
        with current_app.open_resource('sql/schema.sql') as f:
            my_db.executescript(f.read().decode('utf8'))
    except sqlite3.OperationalError as exc:
        print(f"WARNING. Database already set. Caught {exc}")

    
def init_db():
    """
    Initialize database with the schema migrations.
    """
    db = get_db()
    try:
        with current_app.open_resource('sql/schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
    except sqlite3.OperationalError as exc:
        print(f"ERROR! Initializing database. Caught {exc}")


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
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    TODO: Refactor for multiple database drivers.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    If the a database object is on the  global stack, close that object.
    """
    db = g.pop('db', e)

    if db is not None:
        db.close()

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
    Inject init and teardown commands intp flask app object.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
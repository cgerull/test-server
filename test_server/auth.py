"""
auth.py

Authentication module for testserver app.
"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from test_server.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """ Register a new user via UI."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_connection = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db_connection.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db_connection.commit()
            except db_connection.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """ Login via UI."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_connection = get_db()
        error = None
        user = db_connection.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('echo.index'))

        flash(error)

    return render_template('auth/login.html')

# pylint: disable=E0237
@bp.before_app_request
def load_logged_in_user():
    """ Get user from session."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    """ Logout and clear session."""
    session.clear()
    return redirect(url_for('echo.index'))


def login_required(view):
    """ Redirects user to login form if required by page setting."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

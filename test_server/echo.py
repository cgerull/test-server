"""
echo.py

Simple echo response to requester.
Returns simple system information.
    timestamp,
    platform',
    system,
    processor,
    architecture,
    local_ip
    container_name,
    secret,
    remote_ip

URL: /echo
"""

from flask import (
    Blueprint, current_app, render_template, request, flash
)
from flask.helpers import url_for
from werkzeug.utils import redirect

from test_server.persistent_counter import get_redis_connection
from test_server.persistent_counter import increment_redis_counter
from test_server.db import get_db
from test_server.echo_data import EchoData

bp = Blueprint('echo', __name__, url_prefix='/')

@bp.route('/')
def index():
    """ Redirect from / to /echo."""
    return redirect(url_for('.echo'))

@bp.route('/echo', methods=['GET'])
def echo():
    """Build HTML response data and send page to requester."""
    remote_data = EchoData(request)

    page_views = 0
    my_db= get_db()
    error = None
    redis_connection = None
    remote_info = remote_data.get_remote_data()

    if current_app.config['REDIS_SERVER'] is not None:
        redis_connection = get_redis_connection(
            current_app.config['REDIS_SERVER'],
            current_app.config['REDIS_PORT'],
            current_app.config['REDIS_PASSWORD'],
            )

    if redis_connection is not None:
        page_views = increment_redis_counter(
            redis_connection,
            current_app.config['REDIS_HTML_COUNTER'])

    if my_db is not None:
        try:
            my_db.execute(
                "INSERT INTO \
                    req_log (response_code, request_url, request_from_ip) \
                    VALUES (?, ?, ?)",
                (200, request.url, remote_info['RemoteAddr']),
            )
            my_db.commit()
        except my_db.IntegrityError:
            error = "Integgrity error! Can't add record to request log."
        except my_db.OperationalError as err:
            error = f"Can't add record to request log. Error: {err}"

    remote_info = remote_data.get_remote_data()

    if error:
        flash(error)

    return render_template('echo/echo.html',
                echo=remote_info,
                headers=remote_data.get_http_headers(),
                # state=local_data.get_server_state(),
                env={
                        'version': current_app.config['VERSION'],
                        'environment': current_app.config['ENV']
                    },
                page_views=page_views
                )

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
from datetime import datetime
import socket
import platform

from flask import (
    Blueprint, current_app, render_template, request
)
from flask.helpers import url_for
from werkzeug.utils import redirect

from test_server.persistent_counter import get_redis_connection
from test_server.persistent_counter import increment_redis_counter
# from werkzeug.security import check_password_hash, generate_password_hash

# from test_server.db import get_db

bp = Blueprint('echo', __name__, url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('.echo'))

@bp.route('/echo', methods=['GET'])
def echo():
    """Build response data and send page to requester."""
    response_data = build_response_data()
    page_views = 0
    redis_connection = get_redis_connection(
        current_app.config['REDIS_SERVER'],
        current_app.config['REDIS_PORT'],
        current_app.config['REDIS_PASSWORD'],
        )

    if redis_connection:
        page_views = increment_redis_counter(
            redis_connection,
            current_app.config['REDIS_HTML_COUNTER'])

    # resp = make_response(
    #     render_template('index.html',
    #     title=current_app.config['APP_NAME'],
    #     footer=current_app.config['APP_FOOTER'],
    #     resp=response_data,
    #     page_views=page_views)
    #     )
    # resp.headers['Server-IP'] = socket.gethostbyname(hostname)

    return render_template('echo/echo.html',resp=response_data, page_views=page_views)

#
# Utiliy functions
# ############################################################################
def build_response_data():
    """
    Build a dictionary with timestamp, server ip,
    server name, secret and requester ip.
    """
    hostname = socket.gethostname()

    return {
        'now': datetime.now().isoformat(sep=' '),
        'platform': platform.platform(),
        'system': platform.system(),
        'processor': platform.processor(),
        'architecture': ' '.join(map(str,platform.architecture())),
        'local_ip': socket.gethostbyname(hostname),
        'container_name': hostname,
        'secret': get_secret_key(),
        'remote_ip': get_remote_ip()
    }

def get_remote_ip():
    """
    Get client ip address, trying to resolve any
    proxies that modify the request.
    """
    client_ip = ''
    if 'HTTP_X_REAL_IP' in request.environ :
        client_ip = request.environ['HTTP_X_REAL_IP']
    elif 'X_REAL_IP' in request.environ :
        client_ip = request.environ['X_REAL_IP']
    elif 'HTTP_X_FORWARDED_FOR' in request.environ :
        client_ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        client_ip = request.remote_addr

    return client_ip

def get_secret_key():
    """
    Return secret key from:
        Docker secret file or
        Environment variable SECRET_KEY or
        a default value
    """
    secret = ''
    try:
        with open(current_app.config['SECRET_FILE'], mode = 'r', encoding = 'utf_8') as file:
            secret = file.read()
    except IOError:
        # no file, return configured secret
        secret = current_app.config['SECRET_KEY']
    return secret

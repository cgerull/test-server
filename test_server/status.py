"""
status.py

Server system information.
    timestamp,
    uptime,
    platform',
    os-version,

URL: /status
"""
from datetime import datetime
import os
import platform
import socket

from flask import (
    Blueprint, current_app, render_template, request
)
from test_server.local_data import LocalData
# from flask.helpers import url_for
# from werkzeug.utils import redirect

# from test_server.persistent_counter import get_redis_connection
# from test_server.persistent_counter import increment_redis_counter
# from werkzeug.security import check_password_hash, generate_password_hash

# from test_server.db import get_db

bp = Blueprint('status', __name__, url_prefix='/')


@bp.route('/status', methods=['GET'])
# @login_required
def status():
    """Build response data and send page to requester."""
    # response_data = build_response_data()
    local_data = LocalData()
    error = None


    # return render_template('status/status.html',resp=response_data)
    if error:
        flash(error)

    return render_template('status/status.html',
                server_info=local_data.get_server_info(),
                server_state=local_data.get_server_state(),
                # state=local_data.get_server_state(),
                env={
                        'version': current_app.config['VERSION'],
                        'environment': current_app.config['ENV']
                    },
                )
#
# Utiliy functions
# ############################################################################
# def build_response_data():
#     """
#     Build a dictionary with timestamp, server ip,
#     server name, secret and requester ip.
#     """
#     hostname = socket.gethostname()

#     return {
#         'now': datetime.now().isoformat(sep=' '),
#         'platform': platform.platform(),
#         'os_version': platform.version(),
#         'load_average': os.system("uptime | cut -f 4 -d ,"),
#         'hostname' : hostname
#     }

# def get_remote_ip():
#     """
#     Get client ip address, trying to resolve any
#     proxies that modify the request.
#     """
#     client_ip = ''
#     if 'HTTP_X_REAL_IP' in request.environ :
#         client_ip = request.environ['HTTP_X_REAL_IP']
#     elif 'X_REAL_IP' in request.environ :
#         client_ip = request.environ['X_REAL_IP']
#     elif 'HTTP_X_FORWARDED_FOR' in request.environ :
#         client_ip = request.environ['HTTP_X_FORWARDED_FOR']
#     else:
#         client_ip = request.remote_addr

#     return client_ip

# def get_secret_key():
#     """
#     Return secret key from:
#         Docker secret file or
#         Environment variable SECRET_KEY or
#         a default value
#     """
#     secret = ''
#     try:
#         with open(current_app.config['SECRET_FILE'], mode = 'r', encoding = 'utf_8') as file:
#             secret = file.read()
#     except IOError:
#         # no file, return configured secret
#         secret = current_app.config['SECRET_KEY']
#     return secret

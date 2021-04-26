"""
Route module for timeconverter web api
"""
from app import app
from flask import (request, jsonify, render_template, redirect,
                   url_for, flash, make_response)
from datetime import datetime
import socket
import os
import yaml
import platform

from app.redis_tools import get_redis
from app.redis_tools import increment_redis_counter

# Modules constants
localhost = socket.gethostname()
redis_connection = get_redis()

#
# HTML page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Build response data and send page to requester."""
    response_data = build_response_data()
    page_views=0
    if redis_connection:
        increment_redis_counter(redis_connection, app.config['REDIS_HTML_COUNTER'])
        page_views = int(redis_connection.get(app.config['REDIS_HTML_COUNTER']))
    resp = make_response(
        render_template('index.html',
        title=app.config['APP_NAME'],
        footer=app.config['APP_FOOTER'],
        resp=response_data,
        page_views=page_views)
        )
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp


#
# REST API
#######################################################################
@app.route('/api/echo', methods=['GET'])
def api_echo():
    """Build api endpoint for echo data."""
    resp = make_response(jsonify(build_response_data()))
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp


#
# Return configuration
@app.route('/api/config', methods=['GET'])
def api_config():
    """Build api endpoint for config data."""
    resp = make_response(jsonify("Not yet implemented."))
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp

#
# Report the callers IP
@app.route('/api/get-my-ip', methods=['GET'])
def api_get_my_ip():
    """Build api endpoint for config data."""
    # read_config(config_file, srv_config)
    resp = jsonify(get_remote_ip())
    return resp

#
# Responsivness check
@app.route('/ping', methods=['GET'])
def ping():
    """Return alive message."""
    # read_config(config_file, srv_config)
    resp = make_response(jsonify(app.config['PONG']))
    return resp


#
# Utiliy functions
# ############################################################################
def build_response_data():
    """
    Build a dictionary with timestamp, server ip,
    server name, secret and requester ip.
    """
    localhost = socket.gethostname()

    return {
        'now': datetime.now().isoformat(sep=' '),
        'platform': platform.platform(),
        'system': platform.system(),
        'processor': platform.processor(),
        'architecture': ' '.join(map(str,platform.architecture())),
        'local_ip': socket.gethostbyname(localhost),
        'container_name': localhost,
        'secret': get_secret_key(),
        'remote_ip': get_remote_ip()
    }

def get_remote_ip():
    """
    Get client ip address, trying to resolve any
    proxies that modify the request.
    """
    ip = ''
    if 'HTTP_X_REAL_IP' in request.environ :
        ip = request.environ['HTTP_X_REAL_IP']
    elif 'X_REAL_IP' in request.environ :
        ip = request.environ['X_REAL_IP']
    elif 'HTTP_X_FORWARDED_FOR' in request.environ :
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.remote_addr
    
    return ip

def get_secret_key():
    """
    Return secret key from:
        Docker secret file or
        Environment variable SECRET_KEY or
        a default value
    """
    secret = ''
    try:
        f = open(app.config['SECRET_FILE'], 'r')
        secret = f.read()
    except:
        # no file, return configured secret
        secret = app.config['SECRET_KEY']
    return secret

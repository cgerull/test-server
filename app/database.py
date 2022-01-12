"""
MySql atabase module for test server
"""
from app import app
from flask import (request, jsonify, render_template, redirect,
                   url_for, flash, make_response)
from datetime import datetime
import socket
import os
import yaml
import platform
# import PyMySQL
import mysql.connector

# Modules constants
secret_file = '/run/secrets/my_secret_key'
config_file = 'srv-config.yml'
srv_config = {
    'title': 'Testserver',
    'footer': 'Default configuration',
    'ping': 'Testserver is alive'
}
localhost = socket.gethostname()

#
# HTML page
@app.route('/database', methods=['GET', 'POST'])
def db_view():
    """Build response data and send page to requester."""
    read_config(config_file, srv_config)
    response_data = build_response_data()
    resp = make_response(
        render_template('index.html',
        title=srv_config['title'],
        footer=srv_config['footer'],
        resp=response_data)
        )
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp

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

    def get_cursor():
        cursor = None
        try:
            with.mysql.connector.connect(
                host="pi4b",
                user="mysql_user"
                password="mysql_user"
            ) as connection:
                cursor = connection.cursor 
        except Error as e:
            print(e)
        return cursor
        



